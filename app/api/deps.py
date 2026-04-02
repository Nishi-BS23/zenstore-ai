from collections.abc import Generator
from typing import Optional

from sqlalchemy.orm import Session

from app.core.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


def get_current_user_id() -> Optional[int]:
	"""Placeholder dependency for authenticated user context."""
	return None

