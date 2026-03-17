import asyncio
from app.db.session import engine
from app.db.base import Base
from app.models.user import User
from app.models.item import Item
from app.models.event import Event
from app.models.recommendation_cache import RecommendationCache
from app.models.api_key import ApiKey

async def init_models():
    async with engine.begin() as conn:
        # Schema changes must go through Alembic migrations, never drop_all
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created successfully.")

if __name__ == "__main__":
    asyncio.run(init_models())
