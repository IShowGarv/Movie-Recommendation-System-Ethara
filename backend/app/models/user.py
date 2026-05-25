from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class WatchlistItemSchema(BaseModel):
    movie_id: int
    title: str
    added_at: Optional[datetime] = None


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)


class UserResponse(BaseModel):
    name: str
    email: EmailStr


class UserDocument(BaseModel):
    name: str
    email: EmailStr
    password: str
    watchlist: List[WatchlistItemSchema] = []
    search_history: List[str] = []
    created_at: Optional[datetime] = None
