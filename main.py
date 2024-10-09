from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.monitor.monitor import Monitor
from src.helpers.cache_help import cache_popular_sources, fetch_and_monitor_popular_sources


monitor = Monitor()
scheduler = AsyncIOScheduler()


async def main():

    # Кэшируем url самых популярных источников
    scheduler.add_job(
        cache_popular_sources,
        'interval',
        minutes=1,
        misfire_grace_time=10,
    )
    # Кэшируем новости самых популярных источников за последний час
    scheduler.add_job(
        fetch_and_monitor_popular_sources,
        'interval',
        minutes=10,
        misfire_grace_time=10,
        kwargs={'monitor': monitor}
    )
    scheduler.start()
