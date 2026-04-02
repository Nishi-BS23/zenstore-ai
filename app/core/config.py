import os


class Settings:
	PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Zenstore AI API")
	DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./zenstore.db")


settings = Settings()

