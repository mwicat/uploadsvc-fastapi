from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "uploadsvc"
    upload_dir: Path

    model_config = SettingsConfigDict(env_prefix='APP_')
