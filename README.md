# AI-Powered Movie Recommendation Platform

Production-grade movie recommendation stack: offline TF-IDF + cosine similarity ML pipeline, FastAPI backend with Redis caching and JWT auth, and a Next.js frontend.

## Architecture

- **Offline ML** (`ml/`): Feature engineering → TF-IDF → cosine similarity matrix → `.pkl` artifacts in `models/`
- **Online API** (`backend/`): O(1) recommendation lookup, Redis cache (1h TTL), MongoDB users/watchlists
- **Frontend** (`frontend/`): Next.js 14, Redux auth, debounced search, Framer Motion UI

## Quick Start

### 1. Download dataset

From [Kaggle TMDB Movie Metadata](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata), place in `ml/dataset/`:

- `tmdb_5000_movies.csv`
- `tmdb_5000_credits.csv`

### 2. Train ML models

```bash
cd ml
pip install -r requirements.txt
python -c "import nltk; nltk.download('punkt')"
python train.py
```

Outputs: `models/movies_metadata.pkl`, `models/similarity_matrix.pkl`, `models/tfidf_vectorizer.pkl`

### 3. Backend (local)

```bash
cd backend
cp .env.example .env
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Requires MongoDB and Redis running locally, or use Docker Compose.

### 4. Frontend (local)

```bash
cd frontend
cp .env.local.example .env.local
npm install
npm run dev
```

Open http://localhost:3000

### 5. Full stack with Docker

```bash
# From project root — train models first so ./models has .pkl files
docker compose up --build
```

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| API / Swagger | http://localhost:8000/docs |
| Health | http://localhost:8000/health |

## API Endpoints

| Method | Endpoint | Auth |
|--------|----------|------|
| POST | `/api/auth/register` | No |
| POST | `/api/auth/login` | No |
| GET | `/api/movies/popular` | No |
| GET | `/api/movies/search?q=` | No |
| GET | `/api/movies/{id}` | No |
| GET | `/api/recommend?movie_id=` | No |
| GET | `/api/user/watchlist` | Yes |
| POST | `/api/user/watchlist` | Yes |
| DELETE | `/api/user/watchlist/{id}` | Yes |
| GET | `/health` | No |

## Project Structure

```
├── ml/                 # Training pipeline
├── models/             # Serialized models (gitignored)
├── backend/            # FastAPI
├── frontend/           # Next.js
└── docker-compose.yml
```

## Environment Variables

**Backend** (`backend/.env`):

- `MONGO_URI` — MongoDB connection string
- `JWT_SECRET` — Strong secret for JWT signing
- `REDIS_URL` — Redis URL
- `MODELS_DIR` — Path to `.pkl` files (default `../models`)

**Frontend** (`frontend/.env.local`):

- `NEXT_PUBLIC_API_URL` — Backend base URL (default `http://localhost:8000`)

## Roadmap

- TMDB live posters/trailers
- Collaborative filtering from watch history
- Elasticsearch for fuzzy search
- OAuth (NextAuth)
- CI/CD with GitHub Actions
