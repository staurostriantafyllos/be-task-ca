from pydantic_settings import BaseSettings, SettingsConfigDict


class LoggingSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="LOGGING_")

    LEVEL_ROOT: str = "INFO"
    LEVEL_SQLALCHEMY: str = "WARNING"


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DATABASE_")

    CONNECTION_STRING: str
    AUTOCOMMIT: bool = False
    AUTOFLUSH: bool = False
