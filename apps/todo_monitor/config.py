import os
from logging.config import dictConfig

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"simple": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"}},
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "root": {
            "handlers": [
                "console",
            ],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}


KAFKA_CONSUMER_CONFIG = {
    "bootstrap.servers": f"{os.getenv('KAFKA_HOST')}:{os.getenv('KAFKA_PORT')}",
    "group.id": "consumer_group_1",
    "auto.offset.reset": "earliest",
}


def setup_logging() -> None:
    dictConfig(LOGGING)


class DatabaseSettings(BaseSettings):

    model_config = SettingsConfigDict(env_prefix="DB_", env_file=".env", extra="ignore")

    URL: PostgresDsn


class Settings(BaseSettings):
    DB: DatabaseSettings = DatabaseSettings()  # type:ignore[call-arg]


settings = Settings()
