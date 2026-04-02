from functools import lru_cache
from pathlib import Path

try:
	from pydantic_settings import BaseSettings, SettingsConfigDict
except ImportError:  # Compatibility with pydantic v1
	from pydantic import BaseSettings  # type: ignore

	SettingsConfigDict = None  # type: ignore


ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
	DATABASE_URL: str = "sqlite:///./zenstore.db"
	SECRET_KEY: str = "change-me"
	REDIS_URL: str = "redis://localhost:6379/0"

	if SettingsConfigDict is not None:
		model_config = SettingsConfigDict(
			env_file=str(ENV_FILE),
			env_file_encoding="utf-8",
			case_sensitive=True,
		)
	else:
		class Config:
			env_file = str(ENV_FILE)
			case_sensitive = True


@lru_cache
def get_settings() -> Settings:
	return Settings()


settings = get_settings()

