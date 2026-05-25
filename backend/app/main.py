import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.api import auth, movies, recommendations, watchlist
from app.config import settings
from app.core.middleware import RequestLoggingMiddleware
from app.services.engine import ai_engine

logging.basicConfig(level=logging.INFO)

limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongodb_client = AsyncIOMotorClient(settings.MONGO_URI)
    app.db = app.mongodb_client.get_default_database()
    ai_engine.load(settings.MODELS_DIR)
    print("[+] Startup complete")
    yield
    app.mongodb_client.close()
    print("[+] Shutdown complete")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(movies.router, prefix="/api")
app.include_router(recommendations.router, prefix="/api")
app.include_router(watchlist.router, prefix="/api")


@app.get("/health", tags=["Infrastructure"])
def health():
    return {
        "status": "ok",
        "engine_loaded": ai_engine.is_loaded,
        "version": settings.VERSION,
    }


@app.get("/api/movies/trending", tags=["Movies"])
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
def trending(request: Request, limit: int = 20):
    """Alias for popular movies (trending)."""
    return ai_engine.get_popular(top_n=min(limit, 100))
