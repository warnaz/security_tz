from loguru import logger
from email.utils import format_datetime
from datetime import datetime, timedelta, timezone

from src.web.feed import feed_get
from src.db.models import Source
from ..helpers.singleton import Singleton
from ..helpers.constants import FeedStatus
from ..helpers.exceptions import ContentNotFound


class Monitor(Singleton):
    async def _do_monitor_a_feed(self, feed: Source, timeframe: str = "hour"):
        feed_updated_fields = dict()
        now = datetime.now(timezone.utc)

        if feed.last_modified and now < feed.last_modified:
            # Текущие данные актуальны, еще не время))
            return FeedStatus.CACHED

        # Пробуем отправить кэш-запрос
        headers = {
            "If-Modified-Since": format_datetime(feed.last_modified or feed.updated_at)
        }
        if feed.etag:
            # У If-None-Match приоритет перед If-Modified-Since, поэтому запрос будет его юзать
            headers["If-None-Match"] = feed.etag

        wf = await feed_get(feed.url, headers=headers)
        rss_d = wf.clear_content

        try:
            if wf.status == 304:  # cached
                logger.debug(f'Fetched (not updated, cached): {feed.link}')
                return FeedStatus.CACHED

            if rss_d is None:
                raise ContentNotFound()

            wr = wf.web_response
            if (etag := wr.etag) and etag != feed.etag:
                feed_updated_fields["etag"] = etag

            if (last_modified := wr.last_modified) and last_modified != feed.last_modified:
                feed_updated_fields["last_modified"] = last_modified

            if timeframe == "hour":
                time_limit = now - timedelta(hours=1)
            elif timeframe == "day":
                time_limit = now - timedelta(days=1)
            else:
                raise ValueError("Invalid timeframe. Use 'hour' or 'day'.")

            new_entries = [
                entry for entry in rss_d.entries
                if datetime.strptime(entry['published'], '%a, %d %b %Y %H:%M:%S %Z').replace(tzinfo=timezone.utc) > time_limit
            ]

            return new_entries
        except Exception as e:
            raise e
        finally:
            # TODO Записать все в базу, создать CRUD модели для этого
            ...
