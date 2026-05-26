"""
Golden Response - Single-file AI Movie Recommendation Platform

This file combines:
- Offline ML pipeline (TMDB preprocessing + TF-IDF + cosine similarity)
- Runtime recommendation engine
- FastAPI app (auth, movies, recommend, watchlist, health)
- MongoDB and Redis helpers

Usage:
  python goldenresponse.py run              # API + frontend (default)
  python goldenresponse.py run --api-only   # API only
  python goldenresponse.py train            # train with default dataset paths
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from typing import Any

import joblib
import jwt
import pandas as pd
import redis.asyncio as aioredis
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from nltk.stem.snowball import SnowballStemmer
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
GOLDEN_DIR = os.path.join(PROJECT_ROOT, "golden response")
DEFAULT_MODELS_DIR = os.path.join(GOLDEN_DIR, "models")
DEFAULT_MOVIES_CSV = os.path.join(GOLDEN_DIR, "ml", "dataset", "tmdb_5000_movies.csv")
DEFAULT_CREDITS_CSV = os.path.join(GOLDEN_DIR, "ml", "dataset", "tmdb_5000_credits.csv")
FRONTEND_DIR = os.path.join(GOLDEN_DIR, "frontend")


# ----------------------------
# Settings / Config
# ----------------------------
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    PROJECT_NAME: str = "AI Movie Recommendation Platform"
    VERSION: str = "1.0.0"

    MONGO_URI: str = "mongodb://localhost:27017/ai_movies"
    REDIS_URL: str = "redis://localhost:6379"
    MODELS_DIR: str = DEFAULT_MODELS_DIR

    JWT_SECRET: str = "dev_secret_change_in_production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    CACHE_TTL_SECONDS: int = 3600


@lru_cache()
def get_settings() -> Settings:
    s = Settings()
    if not os.path.isabs(s.MODELS_DIR):
        s.MODELS_DIR = os.path.normpath(os.path.join(PROJECT_ROOT, s.MODELS_DIR))
    return s


settings = get_settings()


# ----------------------------
# Security
# ----------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer_scheme = HTTPBearer()


def hash_password(password: str) -> str:
    # bcrypt accepts max 72 bytes
    safe = password.encode("utf-8")[:72].decode("utf-8", errors="ignore")
    return pwd_context.hash(safe)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    payload = data.copy()
    payload["exp"] = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])


# ----------------------------
# Redis Cache
# ----------------------------
_redis_client = None


async def get_redis():
    global _redis_client
    if _redis_client is None:
        _redis_client = await aioredis.from_url(settings.REDIS_URL, decode_responses=True)
    return _redis_client


async def cache_get(key: str):
    try:
        r = await get_redis()
        v = await r.get(key)
        return json.loads(v) if v else None
    except Exception:
        return None


async def cache_set(key: str, value: Any, ttl: int = settings.CACHE_TTL_SECONDS):
    try:
        r = await get_redis()
        await r.setex(key, ttl, json.dumps(value))
    except Exception:
        pass


# ----------------------------
# ML Pipeline
# ----------------------------
stemmer = SnowballStemmer("english")


def parse_json_column(val: str | float, key: str = "name", limit: int | None = None) -> list[str]:
    if pd.isna(val):
        return []
    try:
        data = json.loads(val)
        names = [item[key].strip().lower().replace(" ", "") for item in data]
        return names[:limit] if limit else names
    except Exception:
        return []


def extract_director(crew_val: str | float) -> list[str]:
    if pd.isna(crew_val):
        return []
    try:
        data = json.loads(crew_val)
        return [
            item["name"].strip().lower().replace(" ", "")
            for item in data
            if item.get("job") == "Director"
        ]
    except Exception:
        return []


def normalize_text(text: Any) -> str:
    if not isinstance(text, str):
        return ""
    text = re.sub(r"[^\w\s]", "", text.lower())
    return " ".join(stemmer.stem(word) for word in text.split())


def build_feature_soup(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["genres_clean"] = df["genres"].apply(parse_json_column)
    df["keywords_clean"] = df["keywords"].apply(parse_json_column)
    df["cast_clean"] = df["cast"].apply(lambda x: parse_json_column(x, limit=4))
    df["director_clean"] = df["crew"].apply(extract_director)
    df["overview_clean"] = df["overview"].apply(normalize_text)
    df["tagline_clean"] = df["tagline"].apply(normalize_text)

    def _soup(row) -> str:
        parts = (
            row["genres_clean"]
            + row["keywords_clean"]
            + row["cast_clean"]
            + (row["director_clean"] * 3)
            + [row["overview_clean"]]
            + [row["tagline_clean"]]
        )
        return " ".join(parts)

    df["soup"] = df.apply(_soup, axis=1)
    return df


def train_models(movies_csv: str, credits_csv: str, out_dir: str):
    movies_df = pd.read_csv(movies_csv)
    credits_df = pd.read_csv(credits_csv)
    df = movies_df.merge(credits_df, left_on="id", right_on="movie_id")

    if "title_x" in df.columns:
        df["title"] = df["title_x"]
    if "poster_path" not in df.columns:
        df["poster_path"] = ""

    df = build_feature_soup(df)

    tfidf = TfidfVectorizer(
        stop_words="english",
        max_features=15000,
        min_df=2,
        ngram_range=(1, 2),
    )
    tfidf_matrix = tfidf.fit_transform(df["soup"])
    sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    processed = df[
        [
            "id",
            "title",
            "vote_average",
            "vote_count",
            "release_date",
            "popularity",
            "genres_clean",
            "overview",
            "poster_path",
        ]
    ].copy()
    processed["id"] = processed["id"].astype(int)
    processed = processed.reset_index(drop=True)

    os.makedirs(out_dir, exist_ok=True)
    joblib.dump(processed, os.path.join(out_dir, "movies_metadata.pkl"), compress=3)
    joblib.dump(sim, os.path.join(out_dir, "similarity_matrix.pkl"), compress=5)
    joblib.dump(tfidf, os.path.join(out_dir, "tfidf_vectorizer.pkl"), compress=3)
    print(f"[+] Saved models to {out_dir}")


# ----------------------------
# Recommendation Engine
# ----------------------------
class RecommendationEngine:
    def __init__(self):
        self.movies_df: pd.DataFrame | None = None
        self.similarity_matrix = None
        self._index_map: dict[int, int] = {}
        self.is_loaded = False

    def load(self, models_dir: str):
        meta = os.path.join(models_dir, "movies_metadata.pkl")
        sim = os.path.join(models_dir, "similarity_matrix.pkl")
        if not (os.path.exists(meta) and os.path.exists(sim)):
            print("[-] Model files not found; fallback mode enabled")
            return
        self.movies_df = joblib.load(meta)
        self.similarity_matrix = joblib.load(sim)
        self._index_map = {int(r["id"]): i for i, r in self.movies_df.iterrows()}
        self.is_loaded = True
        print(f"[+] Engine loaded: {len(self.movies_df)} movies")

    def _row(self, r: pd.Series, score: float | None = None) -> dict[str, Any]:
        out = {
            "movie_id": int(r["id"]),
            "title": str(r["title"]),
            "vote_average": float(r["vote_average"]),
            "popularity": float(r.get("popularity", 0)),
            "release_date": str(r.get("release_date", "") or ""),
            "overview": str(r.get("overview", "") or ""),
            "poster_path": (str(r.get("poster_path", "") or "") or None),
            "genres": r.get("genres_clean", []) if isinstance(r.get("genres_clean", []), list) else [],
        }
        if score is not None:
            out["confidence_score"] = round(float(score), 4)
        return out

    def get_popular(self, top_n: int = 20) -> list[dict[str, Any]]:
        if self.movies_df is None:
            return []
        top = self.movies_df.nlargest(top_n, "popularity")
        return [{**self._row(r), "confidence_score": 0.5} for _, r in top.iterrows()]

    def get_movie(self, movie_id: int) -> dict[str, Any] | None:
        if self.movies_df is None:
            return None
        i = self._index_map.get(movie_id)
        if i is None:
            return None
        return self._row(self.movies_df.iloc[i])

    def search(self, query: str, top_n: int = 10) -> list[dict[str, Any]]:
        if self.movies_df is None:
            return []
        q = query.lower().strip()
        mask = self.movies_df["title"].str.lower().str.contains(q, na=False)
        return [self._row(r) for _, r in self.movies_df[mask].head(top_n).iterrows()]

    def recommend(self, movie_id: int, top_n: int = 10) -> list[dict[str, Any]]:
        if not self.is_loaded:
            return self.get_popular(top_n)
        idx = self._index_map.get(movie_id)
        if idx is None:
            return []
        scores = list(enumerate(self.similarity_matrix[idx]))
        scores.sort(key=lambda x: x[1], reverse=True)
        out = []
        for i, s in scores[1 : top_n + 1]:
            out.append(self._row(self.movies_df.iloc[i], s))
        return out


ai_engine = RecommendationEngine()


# ----------------------------
# API Schemas
# ----------------------------
class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    password: str = Field(..., min_length=6)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class WatchlistItem(BaseModel):
    movie_id: int
    title: str = Field(..., min_length=1)


# ----------------------------
# Dependency Helpers
# ----------------------------
def _get_db_from_app() -> AsyncIOMotorDatabase:
    return app.db


async def get_db() -> AsyncIOMotorDatabase:
    return _get_db_from_app()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    try:
        payload = decode_token(credentials.credentials)
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate token")

    user = await db["users"].find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ----------------------------
# Routers
# ----------------------------
auth_router = APIRouter(prefix="/api/auth", tags=["Authentication"])
movies_router = APIRouter(prefix="/api/movies", tags=["Movies"])
reco_router = APIRouter(prefix="/api/recommend", tags=["Recommendations"])
watchlist_router = APIRouter(prefix="/api/user/watchlist", tags=["Watchlist"])


@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest, db: AsyncIOMotorDatabase = Depends(get_db)):
    if await db["users"].find_one({"email": payload.email}):
        raise HTTPException(status_code=409, detail="Email already registered")
    await db["users"].insert_one(
        {
            "name": payload.name,
            "email": payload.email,
            "password": hash_password(payload.password),
            "watchlist": [],
            "search_history": [],
            "created_at": datetime.now(timezone.utc),
        }
    )
    return {"message": "Account created successfully"}


@auth_router.post("/login")
async def login(payload: LoginRequest, db: AsyncIOMotorDatabase = Depends(get_db)):
    user = await db["users"].find_one({"email": payload.email})
    if not user or not verify_password(payload.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token({"sub": user["email"]})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"name": user["name"], "email": user["email"]},
    }


@movies_router.get("/popular")
def popular(limit: int = Query(20, ge=1, le=100)):
    return ai_engine.get_popular(limit)


@movies_router.get("/search")
def search(q: str = Query(..., min_length=1), limit: int = Query(10, ge=1, le=50)):
    return ai_engine.search(q, limit)


@movies_router.get("/{movie_id}")
def movie_detail(movie_id: int):
    movie = ai_engine.get_movie(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail=f"Movie {movie_id} not found")
    return movie


@reco_router.get("", include_in_schema=False)
@reco_router.get("/")
async def recommend(
    movie_id: int = Query(..., description="TMDB movie ID"),
    limit: int = Query(10, ge=1, le=50),
):
    key = f"reco:{movie_id}:{limit}"
    cached = await cache_get(key)
    if cached:
        return cached
    recs = ai_engine.recommend(movie_id, limit)
    if not recs:
        raise HTTPException(status_code=404, detail=f"No recommendations for {movie_id}")
    await cache_set(key, recs)
    return recs


@watchlist_router.get("/")
async def get_watchlist(
    current_user=Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    user = await db["users"].find_one({"email": current_user["email"]})
    return {"watchlist": user.get("watchlist", [])}


@watchlist_router.post("/")
async def add_watchlist(
    item: WatchlistItem,
    current_user=Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    doc = {
        "movie_id": item.movie_id,
        "title": item.title,
        "added_at": datetime.now(timezone.utc),
    }
    await db["users"].update_one(
        {"email": current_user["email"]},
        {"$addToSet": {"watchlist": doc}},
    )
    return {"message": f"'{item.title}' added to watchlist"}


@watchlist_router.delete("/{movie_id}")
async def remove_watchlist(
    movie_id: int,
    current_user=Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    await db["users"].update_one(
        {"email": current_user["email"]},
        {"$pull": {"watchlist": {"movie_id": movie_id}}},
    )
    return {"message": "Removed from watchlist"}


# ----------------------------
# FastAPI App
# ----------------------------
@asynccontextmanager
async def lifespan(api: FastAPI):
    api.mongodb_client = AsyncIOMotorClient(settings.MONGO_URI)
    api.db = api.mongodb_client.get_default_database()
    ai_engine.load(settings.MODELS_DIR)
    yield
    api.mongodb_client.close()


app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(movies_router)
app.include_router(reco_router)
app.include_router(watchlist_router)


@app.get("/health", tags=["Infrastructure"])
def health():
    return {"status": "ok", "engine_loaded": ai_engine.is_loaded, "version": settings.VERSION}


# ----------------------------
# CLI entrypoint
# ----------------------------
def _ensure_models() -> bool:
    meta = os.path.join(settings.MODELS_DIR, "movies_metadata.pkl")
    sim = os.path.join(settings.MODELS_DIR, "similarity_matrix.pkl")
    if os.path.exists(meta) and os.path.exists(sim):
        return True

    if not (os.path.exists(DEFAULT_MOVIES_CSV) and os.path.exists(DEFAULT_CREDITS_CSV)):
        print("[-] Models missing and dataset CSV files not found.")
        print(f"    Place CSVs in: {os.path.dirname(DEFAULT_MOVIES_CSV)}")
        return False

    print("[*] Models not found. Training now...")
    train_models(DEFAULT_MOVIES_CSV, DEFAULT_CREDITS_CSV, settings.MODELS_DIR)
    return True


def run_api(host: str, port: int, reload: bool):
    import uvicorn

    os.environ["MODELS_DIR"] = settings.MODELS_DIR
    print(f"[*] API: http://{host}:{port}")
    print(f"[*] Docs: http://{host}:{port}/docs")
    print(f"[*] Models: {settings.MODELS_DIR}")
    uvicorn.run("goldenresponse:app", host=host, port=port, reload=reload)


def run_frontend():
    if not os.path.isdir(FRONTEND_DIR):
        print(f"[-] Frontend folder not found: {FRONTEND_DIR}")
        return None

    env = os.environ.copy()
    env["NEXT_PUBLIC_API_URL"] = "http://localhost:8000"
    print(f"[*] Frontend: http://localhost:3000")
    return subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=FRONTEND_DIR,
        env=env,
        shell=True,
    )


def run_project(host: str, port: int, reload: bool, api_only: bool):
    if not _ensure_models():
        sys.exit(1)

    frontend_proc = None
    if not api_only:
        frontend_proc = run_frontend()
        time.sleep(2)

    try:
        run_api(host=host, port=port, reload=reload)
    finally:
        if frontend_proc and frontend_proc.poll() is None:
            frontend_proc.terminate()


def main():
    parser = argparse.ArgumentParser(
        description="Golden Response - run the full movie recommendation project"
    )
    sub = parser.add_subparsers(dest="cmd")

    run_p = sub.add_parser("run", help="Run API and frontend (default)")
    run_p.add_argument("--host", default="0.0.0.0")
    run_p.add_argument("--port", type=int, default=8000)
    run_p.add_argument("--reload", action="store_true", help="Enable API auto-reload")
    run_p.add_argument("--api-only", action="store_true", help="Start API only")

    train_p = sub.add_parser("train", help="Train and export model files")
    train_p.add_argument("--movies", default=DEFAULT_MOVIES_CSV)
    train_p.add_argument("--credits", default=DEFAULT_CREDITS_CSV)
    train_p.add_argument("--out", default=DEFAULT_MODELS_DIR)

    args = parser.parse_args()
    cmd = args.cmd or "run"

    if cmd == "train":
        train_models(args.movies, args.credits, args.out)
    elif cmd == "run":
        run_project(
            host=args.host,
            port=args.port,
            reload=args.reload,
            api_only=args.api_only,
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
