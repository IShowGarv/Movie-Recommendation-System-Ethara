from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel, Field

from app.core.deps import get_current_user, get_db
from app.services import watchlist as watchlist_service

router = APIRouter(prefix="/user/watchlist", tags=["Watchlist"])


class WatchlistItem(BaseModel):
    movie_id: int
    title: str = Field(..., min_length=1)


@router.get("/")
async def get_watchlist(
    current_user=Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    items = await watchlist_service.get_user_watchlist(db, current_user["email"])
    return {"watchlist": items}


@router.post("/")
async def add_to_watchlist(
    item: WatchlistItem,
    current_user=Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    await watchlist_service.add_watchlist_item(
        db, current_user["email"], item.movie_id, item.title
    )
    return {"message": f"'{item.title}' added to watchlist"}


@router.delete("/{movie_id}")
async def remove_from_watchlist(
    movie_id: int,
    current_user=Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    await watchlist_service.remove_watchlist_item(
        db, current_user["email"], movie_id
    )
    return {"message": "Removed from watchlist"}
