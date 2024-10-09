from typing import List, Optional
import redis
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from loguru import logger

from src.db.crud import get_most_popular_sources, get_source_by_id
from src.monitor.monitor import Monitor
from config.config import cache_settings


redis = Redis()


async def cache_popular_sources():
    """Кэширует ID и URL самых популярных источников в Redis."""
    popular_sources: List[dict] = await get_most_popular_sources()

    for source in popular_sources:
        source_id = source['id']
        source_url = source['url']

        await redis.hset(
            name="popular_sources",
            key=source_id,
            value=source_url,
        )
        logger.info(f"Источник {source_url} с ID {source_id} кэширован.")


async def fetch_and_monitor_popular_sources(monitor: Monitor, timeframe: str = "hour"):
    """Извлекает кэшированные популярные источники и запускает мониторинг. Добавляет в кэш новости"""
    source_ids = await redis.hkeys("popular_sources")

    for source_id in source_ids:
        source_url = await redis.hget("popular_sources", source_id)

        if source_url:
            try:
                source_obj = await get_source_by_id(source_id.decode('utf-8'))

                if source_obj:
                    data = await monitor._do_monitor_a_feed(source_obj, timeframe=timeframe)
                    if data:
                        for news in data:
                            news_summary = {
                                'title': news.get('title', ''),
                                'link': news.get('link', ''),
                                'summary': news.get('summary', ''),
                                'published': news.get('published', ''),
                            }
                            await redis.hset(
                                name=f"source_data:{source_id.decode('utf-8')}",
                                key=source_id.decode('utf-8'),
                                value=news_summary,
                            )
                            await redis.expire(f"source_data:{source_id.decode('utf-8')}", cache_settings.DEFAULT_TTL)
                            logger.info(
                                f"Данные для источника {source_url.decode('utf-8')} кэшированы в Redis.")
                    else:
                        logger.warning(
                            f"Нет новых данных для источника {source_url.decode('utf-8')}.")
                else:
                    logger.warning(
                        f"Source id: {source_id.decode('utf-8')} не найден в базе.")
            except Exception as e:
                logger.error(
                    f"Ошибка при обработке источника {source_url.decode('utf-8')}: {str(e)}")


async def get_cached_news(source_ids: List[str]) -> List[dict]:
    """Получает новости из кэша для заданных источников."""
    cached_news = []

    for source_id in source_ids:
        news_data = await redis.hgetall(f"source_data:{source_id}")
        if news_data:
            cached_news.append(news_data)

    return cached_news
