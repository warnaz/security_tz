from aio_pika import connect, ExchangeType
import asyncio
import redis

from src.monitor import Monitor

from .process_sources import process_remaining_sources
from src.helpers.cache_help import get_cached_news


async def handle_get_news(user_id: str, monitor: Monitor) -> None:
    """Обрабатывает запрос пользователя на получение новостей за последний час."""
    source_ids = await redis.hkeys("popular_sources")

    cached_news = await get_cached_news(source_ids)

    await send_news_to_user(user_id, cached_news)

    remaining_source_ids = [
        source_id for source_id in source_ids if source_id not in cached_news]

    async for news in process_remaining_sources(monitor, remaining_source_ids):
        await send_news_to_user(user_id, [news])


async def run_handle():
    connection = await connect("amqp://guest:guest@localhost/")
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue('news_queue')

        async for message in queue:
            await process_message(message)
