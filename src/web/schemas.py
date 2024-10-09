import feedparser
from dataclasses import dataclass
from typing import AnyStr, Optional

from multidict import CIMultiDictProxy


@dataclass
class WebResponse:
    url: str
    content: bytes  # байты меньше места занимают, чем строка))
    headers: CIMultiDictProxy[str]
    status: int
    reason: Optional[str]
    last_modified: Optional[str] = None

    @property
    def etag(self) -> Optional[str]:
        return self.headers.get('ETag')


@dataclass
class WebFeed:
    url: str
    content: Optional[AnyStr] = None
    headers: Optional[CIMultiDictProxy[str]] = None
    status: int = -1
    reason: Optional[str] = None
    clear_content: Optional[feedparser.FeedParserDict] = None

    # схему новую добавить со статусами тоже, если ошибки разные будут
    error: Optional[str] = None

    web_response: Optional[WebResponse] = None
