from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, select

from db.models import UserSource, Source
from config.config import settings


DATABASE_URL = settings.DATABASE_URL
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False)


def session_decorator(func):
    async def wrapper(*args, **kwargs):
        async with AsyncSessionLocal() as session:
            kwargs['db'] = session
            return await func(*args, **kwargs)
    return wrapper


@session_decorator
async def get_most_popular_sources(db: AsyncSession, limit: int = 10) -> List[dict]:
    '''Получаем список популярных источников асинхронно'''

    popular_sources = (
        await db.execute(
            select(Source.id, Source.url)
            .join(UserSource, Source.id == UserSource.source_id)
            .group_by(Source.id)
            .order_by(func.count(UserSource.source_id).desc())
            .limit(limit)
        )
    )

    return [{'id': row[0], 'url': row[1]} for row in popular_sources]


@session_decorator
async def get_source_by_id(db: AsyncSession, source_id: int) -> Optional[Source]:
    result = await db.execute(select(Source).where(Source.id == source_id))
    return result.scalar_one_or_none()
