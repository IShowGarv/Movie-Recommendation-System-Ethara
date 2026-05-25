from datetime import datetime, timezone

from motor.motor_asyncio import AsyncIOMotorDatabase


async def get_user_watchlist(db: AsyncIOMotorDatabase, email: str):
    user = await db["users"].find_one({"email": email})
    if not user:
        return []
    return user.get("watchlist", [])


async def add_watchlist_item(
    db: AsyncIOMotorDatabase, email: str, movie_id: int, title: str
):
    item = {
        "movie_id": movie_id,
        "title": title,
        "added_at": datetime.now(timezone.utc),
    }
    await db["users"].update_one(
        {"email": email},
        {"$addToSet": {"watchlist": item}},
    )
    return item


async def remove_watchlist_item(db: AsyncIOMotorDatabase, email: str, movie_id: int):
    await db["users"].update_one(
        {"email": email},
        {"$pull": {"watchlist": {"movie_id": movie_id}}},
    )
