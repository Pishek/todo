from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):

    model_config = SettingsConfigDict(env_prefix="DB_", env_file=".env", extra="ignore")

    URL: PostgresDsn


class KafkaConsumerSettings(BaseSettings):

    model_config = SettingsConfigDict(env_prefix="KAFKA_", env_file=".env", extra="ignore")

    HOST: str
    PORT: str
    GROUP_ID: str


class Settings(BaseSettings):
    DB: DatabaseSettings = DatabaseSettings()  # type:ignore[call-arg]
    KAFKA: KafkaConsumerSettings = KafkaConsumerSettings()  # type:ignore[call-arg]


settings = Settings()
