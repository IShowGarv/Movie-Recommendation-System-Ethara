from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, Query

from app.services.engine import ai_engine

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get("/popular", response_model=List[Dict[str, Any]])
def popular(limit: int = Query(20, ge=1, le=100)):
    """Returns top movies sorted by popularity score."""
    return ai_engine.get_popular(top_n=limit)


@router.get("/search", response_model=List[Dict[str, Any]])
def search(q: str = Query(..., min_length=1), limit: int = Query(10, ge=1, le=50)):
    """Title-based movie search with partial and case-insensitive matching."""
    return ai_engine.search_by_title(query=q, top_n=limit)


@router.get("/{movie_id}", response_model=Dict[str, Any])
def get_movie(movie_id: int):
    """Returns metadata for a single movie."""
    movie = ai_engine.get_movie_by_id(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail=f"Movie {movie_id} not found")
    return movie
