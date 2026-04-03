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


def _create_token(user_id: str, token_type: str, expires_delta: timedelta) -> str:
	"""Create a signed JWT token with user and token type claims."""
	expire = datetime.now(timezone.utc) + expires_delta
	payload: dict[str, Any] = {
		"sub": user_id,
		"typ": token_type,
		"exp": expire,
		"iat": datetime.now(timezone.utc),
	}
	encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)
	return encoded_jwt


def create_access_token(user_id: str, expires_delta: timedelta | None = None) -> str:
	"""Create access token for API authorization."""
	if expires_delta is None:
		expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
	return _create_token(user_id=user_id, token_type="access", expires_delta=expires_delta)


def create_refresh_token(user_id: str, expires_delta: timedelta | None = None) -> str:
	"""Create refresh token used to obtain a new access token."""
	if expires_delta is None:
		expires_delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
	return _create_token(user_id=user_id, token_type="refresh", expires_delta=expires_delta)


def create_jwt_token(user_id: str, expires_delta: timedelta | None = None) -> str:
	"""Backward-compatible wrapper for access token generation."""
	return create_access_token(user_id=user_id, expires_delta=expires_delta)


def decode_jwt_token(token: str) -> dict[str, Any]:
	"""Decode and verify JWT token, return payload."""
	decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
	return decoded


def is_refresh_token(payload: dict[str, Any]) -> bool:
	"""Return True when payload represents a refresh token."""
	return payload.get("typ") == "refresh"

