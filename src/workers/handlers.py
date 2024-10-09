import asyncio
from loguru import logger
from aio_pika import Message, ExchangeType

from src.monitor import Monitor
from src.services.handle_sources import handle_get_news


async def process_message(message: Message):
    async with message.process():
        user_id = message.body.decode()
        monitor = Monitor()

        try:
            await handle_get_news(user_id, monitor)  # Вызовите вашу функцию
        except Exception as e:
            logger.error(
                f"Ошибка обработки новостей для пользователя {user_id}: {e}")
