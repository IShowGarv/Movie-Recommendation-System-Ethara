# AI-Powered Movie Recommendation Platform

Production-grade movie recommendation stack: offline TF-IDF + cosine similarity ML pipeline, FastAPI backend with Redis caching and JWT auth, and a Next.js frontend.

## Project Structure

```
├── golden response/          # Full implementation (backend, frontend, ml, models)
│   ├── backend/
│   ├── frontend/
│   ├── ml/
│   ├── models/
│   ├── docker-compose.yml
│   └── start.ps1
├── goldenresponse.py         # Single-file runner (train + run full stack)
├── prompt.md                 # Complete system prompt / requirements
└── justification.md          # Evaluation and golden response rationale
```

## Quick Start (Recommended)

```powershell
cd "Ethara Task"
python goldenresponse.py run
```

- App: http://localhost:3000
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

Or use:

```powershell
.\golden response\start.ps1
```

## Train Models

Place TMDB CSV files in `golden response/ml/dataset/`, then:

```powershell
python goldenresponse.py train
```

## Manual Start

```powershell
# Backend
cd "golden response/backend"
pip install -r requirements.txt
$env:MODELS_DIR="..\models"
uvicorn app.main:app --reload --port 8000

# Frontend
cd "golden response/frontend"
npm install
npm run dev
```

## Docker

```bash
cd "golden response"
docker compose up --build
```

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

## Repository

https://github.com/IShowGarv/Movie-Recommendation-System-Ethara
