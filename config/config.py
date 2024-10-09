from typing import Optional
from dotenv import load_dotenv
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn
    BOT_TOKEN: str

    LOG_LEVEL: str = "INFO"


class WebSettings(BaseSettings):
    PROXY: Optional[str] = None
    HTTP_TIMEOUT: int = 12
    MAX_RETRIES: int = 3


class CacheSettings(BaseSettings):
    DEFAULT_TTL: int = 600


settings = Settings()
web_settings = WebSettings()
cache_settings = CacheSettings()
