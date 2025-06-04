from dotenv import load_dotenv
load_dotenv()
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

DATABASE_URL = settings.DATABASE_URL
REDIS_URL = settings.REDIS_URL
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
