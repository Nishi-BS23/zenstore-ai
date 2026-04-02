from collections.abc import Generator
from typing import Optional

import jwt
from fastapi import Depends, HTTPException, Header, status
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.security import decode_jwt_token
from app.models.user import User


def get_db() -> Generator[Session, None, None]:
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


def get_current_user_id() -> Optional[int]:
	"""Placeholder dependency for authenticated user context."""
	return None


def get_current_user(
	db: Session = Depends(get_db),
	authorization: Optional[str] = Header(None),
) -> User:
	"""Dependency to get current authenticated user from JWT token."""
	if not authorization:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Missing authorization header",
		)

	try:
		scheme, token = authorization.split()
		if scheme.lower() != "bearer":
			raise ValueError("Invalid scheme")
	except ValueError:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Invalid authorization header format",
		)

	try:
		payload = decode_jwt_token(token)
		user_id = payload.get("sub")
		if not user_id:
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail="Invalid token",
			)
	except jwt.ExpiredSignatureError:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Token expired",
		)
	except jwt.InvalidTokenError:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Invalid token",
		)

	user = db.query(User).filter(User.id == user_id).first()
	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="User not found",
		)

	return user

