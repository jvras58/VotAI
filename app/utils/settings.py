"""Settings management for the application using Pydantic."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Class that represents the settings set in the application's .env.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        env_ignore_empty=True,
    )

    CLIENT_ID_GOOGLE: str
    SECRET_GOOGLE: str
    SWAGGER_DOCS_ROUTE: str = "/docs"
    SWAGGER_REDOCS_ROUTE: str = "/redoc"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    # Secret key for session management (used in SessionMiddleware)
    SESSION_SECRET_KEY: str = "change-me-in-production"


@lru_cache
def get_settings() -> Settings:
    """Get the application settings, cached for performance."""
    return Settings()
