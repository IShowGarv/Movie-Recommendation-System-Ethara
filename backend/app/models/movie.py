from typing import List, Optional

from pydantic import BaseModel, Field


class MovieResponse(BaseModel):
    movie_id: int
    title: str
    vote_average: float
    popularity: float = 0.0
    release_date: str = ""
    overview: str = ""
    confidence_score: Optional[float] = None
    poster_path: Optional[str] = None
    genres: List[str] = Field(default_factory=list)


class MovieDetail(MovieResponse):
    vote_count: Optional[int] = None
