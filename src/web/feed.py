import asyncio
import feedparser
from loguru import logger

from .req import get
from .utils import FEED_ACCEPT, get_user_agent
from .schemas import WebFeed, WebResponse


async def feed_get(
    url: str,
    headers: dict = None,
    timeout: float = None,
    web_semaphore: asyncio.Semaphore = None,
) -> WebFeed:

    ret = WebFeed(url=url)

    _headers = {}

    if headers:
        _headers.update(headers)
    if 'Accept' not in _headers:
        _headers['Accept'] = FEED_ACCEPT

    _headers['User-Agent'] = get_user_agent()

    try:
        resp: WebResponse = await get(url, timeout, web_semaphore, headers=_headers)
        rss_content = resp.content
        ret.content = rss_content
        ret.url = resp.url
        ret.headers = resp.headers
        ret.status = resp.status
        ret.web_response = resp

        # некоторые RSS-каналы неправильно реализуют http-кеширование
        if resp.status == 200 and int(resp.headers.get('Content-Length', '1')) == 0:
            ret.status = 304
            return ret

        if resp.status == 304:
            return ret

        if rss_content is None:
            status_caption = f'{resp.status} {resp.reason}'
            ret.error = status_caption
            return ret

        content = feedparser.parse(
            ret.content,
            response_headers={k.lower(): v for k, v in resp.headers.items()}
        )

        # Проверка наличия ошибок во время парсинга
        if not content.feed.get('title'):
            if not content.entries and (content.bozo or not (content.feed.get('link') or content.feed.get('updated'))):
                ret.error = 'Invalid feed'
                return ret
            content.feed['title'] = resp.url

        ret.clear_content = content
    except Exception as e:
        logger.error(e)
        ret.error = str(e)

    return ret
