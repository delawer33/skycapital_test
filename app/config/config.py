from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, PostgresDsn
from pathlib import Path


class Settings(BaseSettings):
    APP_NAME: str = "task_manager"
    DEBUG: bool = True

    DB_URL: PostgresDsn = (
        
    )

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / ".env", extra="ignore"
    )
