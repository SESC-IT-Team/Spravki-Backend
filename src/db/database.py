import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import settings

print("DB_HOST:", settings.DB_HOST)
print("DB_NAME:", settings.DB_NAME)
print("CONTAINER:", os.getenv("HOSTNAME"))

DATABASE_URL = (
    f"postgresql+asyncpg://"
    f"{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
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
