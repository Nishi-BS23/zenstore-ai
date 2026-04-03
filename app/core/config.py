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
	ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
	REFRESH_TOKEN_EXPIRE_DAYS: int = 7
	REDIS_URL: str = "redis://localhost:6379/0"
	AI_PROVIDER: str = "groq"
	AI_MODEL: str = "llama-3.1-8b-instant"
	GROQ_API_KEY: str = ""
	OPENAI_API_KEY: str = ""
	OPENAI_BASE_URL: str = "https://api.openai.com/v1"

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

