from sqlalchemy import QueuePool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

DATABASE_URL = settings.POSTGRES_URL
DATABASE_PARAMS = {
    "poolclass": QueuePool,
}

engine = create_async_engine(url=DATABASE_URL, echo=False, **DATABASE_PARAMS)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
