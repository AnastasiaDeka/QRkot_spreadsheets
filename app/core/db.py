from typing import AsyncGenerator

from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from app.core.config import settings


class PreBase:
    """Базовый класс с именем таблицы и первичным ключом."""

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.database_url)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Асинхронно выдаёт сессию БД."""
    async with AsyncSessionLocal() as session:
        yield session
