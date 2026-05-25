from typing import Any, Dict, List

from app.services.engine import ai_engine


def fuzzy_search_movies(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Title search via in-memory DataFrame; swap for Elasticsearch in production."""
    if not query.strip():
        return []
    return ai_engine.search_by_title(query=query, top_n=limit)
