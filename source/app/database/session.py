from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from app.config import get_settings, Config
from app.database.models.base import Base

config = get_settings()

metadata = Base.metadata


engine = create_async_engine(
    config.database_url,
)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncSession:
    """
    Dependency function that yields db sessions
    """
    async with async_session() as session:
        yield session
        await session.commit()
