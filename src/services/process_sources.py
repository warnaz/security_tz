from typing import List
from loguru import logger

from src.monitor.monitor import Monitor
from src.db.crud import get_source_by_id


async def process_remaining_sources(monitor: Monitor, remaining_source_ids: List[str], timeframe: str = "hour"):
    """Обрабатывает оставшиеся источники и возвращает данные по мере их получения."""
    for source_id in remaining_source_ids:
        try:
            source_obj = await get_source_by_id(source_id)
            if source_obj:
                data = await monitor._do_monitor_a_feed(source_obj, timeframe)
                if data:
                    for news in data:
                        news_summary = {
                            'title': news.get('title', ''),
                            'link': news.get('link', ''),
                            'summary': news.get('summary', ''),
                            'published': news.get('published', ''),
                        }
                        yield news_summary
                else:
                    logger.warning(
                        f"Нет новых данных для источника {source_id}.")
            else:
                logger.warning(f"Source id: {source_id} не найден в базе.")
        except Exception as e:
            logger.error(
                f"Ошибка при обработке источника {source_id}: {str(e)}")
