from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, Query

from app.core.cache import cache_get, cache_set
from app.services.engine import ai_engine

router = APIRouter(prefix="/recommend", tags=["Recommendations"])


@router.get("/", response_model=List[Dict[str, Any]])
async def recommend(
    movie_id: int = Query(..., description="TMDB movie ID"),
    limit: int = Query(10, ge=1, le=50, description="Number of recommendations"),
):
    """Returns AI-powered content-based recommendations for a given movie."""
    cache_key = f"reco:{movie_id}:{limit}"

    cached = await cache_get(cache_key)
    if cached:
        return cached

    recommendations = ai_engine.get_recommendations(movie_id=movie_id, top_n=limit)

    if not recommendations:
        raise HTTPException(
            status_code=404,
            detail=f"No recommendations found for movie_id={movie_id}",
        )

    await cache_set(cache_key, recommendations)
    return recommendations
