from typing import Final
from fake_useragent import UserAgent


FEED_ACCEPT: Final = 'application/rss+xml'


def get_user_agent():
    return UserAgent().random
