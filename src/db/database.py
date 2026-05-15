import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import settings

DATABASE_URL = (
    f"postgresql+asyncpg://"
    f"{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
    f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_NAME}"
)


engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)



async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)

Base = declarative_base()


async def get_session() -> "AsyncGenerator[AsyncSession, None]":
    async with async_session() as session:
        yield session
