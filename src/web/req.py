import asyncio
import aiohttp

from functools import partial
from typing import Callable, Optional

from config.config import web_settings
from .schemas import WebResponse


async def request(
        method: str,
        url: str,
        timeout: Optional[float] = None,
        semaphore: Optional[asyncio.Semaphore] = None,
        headers: Optional[dict] = None,
) -> WebResponse:
    if timeout is None:
        timeout = web_settings.HTTP_TIMEOUT

    async def _fetch():
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.request(method, url) as response:
                status = response.status
                content = await response.read() if status == 200 else None
                return WebResponse(
                    url=url,
                    content=content,
                    headers=response.headers,
                    status=status,
                    reason=response.reason,
                    last_modified=response.headers.get('Last-Modified'),
                )

    tries = 0
    while tries < web_settings.MAX_RETRIES:
        tries += 1

        if semaphore:
            async with semaphore:
                return await asyncio.wait_for(_fetch(), timeout)

        return await asyncio.wait_for(_fetch(), timeout)

    raise Exception("Max retries exceeded")


get: Callable = partial(request, aiohttp.hdrs.METH_GET)
