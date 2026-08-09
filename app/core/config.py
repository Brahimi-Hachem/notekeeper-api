from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # provide a default so instantiating Settings() without explicit args
    # (e.g. during static analysis or when env file is missing) won't raise
    # an error. The real value can still be loaded from the .env at runtime.
    database_url: str = (
        "postgresql+psycopg://notekeeper:notekeeper_dev@localhost:5432/notekeeper"
    )
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
