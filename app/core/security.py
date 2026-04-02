from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt
import jwt

from app.core.config import settings


ALGORITHM = "HS256"


def hash_password(password: str) -> str:
	"""Hash password using bcrypt."""
	salt = bcrypt.gensalt(rounds=12)
	hashed = bcrypt.hashpw(password.encode(), salt)
	return hashed.decode()


def verify_password(password: str, hashed_password: str) -> bool:
	"""Verify password against bcrypt hash."""
	return bcrypt.checkpw(password.encode(), hashed_password.encode())


def create_jwt_token(user_id: str, expires_delta: timedelta | None = None) -> str:
	"""Create JWT token with user_id as 'sub' claim."""
	if expires_delta is None:
		expires_delta = timedelta(hours=24)

	expire = datetime.now(timezone.utc) + expires_delta
	payload: dict[str, Any] = {
		"sub": user_id,
		"exp": expire,
		"iat": datetime.now(timezone.utc),
	}
	encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)
	return encoded_jwt


def decode_jwt_token(token: str) -> dict[str, Any]:
	"""Decode and verify JWT token, return payload."""
	decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
	return decoded

