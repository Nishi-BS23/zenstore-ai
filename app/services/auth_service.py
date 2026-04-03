from sqlalchemy.orm import Session

import jwt

from app.core.security import (
	create_access_token,
	create_refresh_token,
	decode_jwt_token,
	hash_password,
	is_refresh_token,
	verify_password,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository


class AuthService:
	"""Service for authentication operations."""

	@staticmethod
	def register_user(email: str, password: str, db: Session) -> User:
		"""Register a new user."""
		repo = UserRepository(db)
		existing = repo.get_by_email(email)
		if existing:
			raise ValueError(f"User with email {email} already exists")

		hashed_pwd = hash_password(password)
		return repo.create(email=email, hashed_password=hashed_pwd)

	@staticmethod
	def login_user(email: str, password: str, db: Session) -> tuple[User, str, str]:
		"""Authenticate user and return user + access/refresh tokens."""
		repo = UserRepository(db)
		user = repo.get_by_email(email)
		if not user:
			raise ValueError("Invalid email or password")

		if not verify_password(password, user.hashed_password):
			raise ValueError("Invalid email or password")

		access_token = create_access_token(user.id)
		refresh_token = create_refresh_token(user.id)
		return user, access_token, refresh_token

	@staticmethod
	def refresh_access_token(refresh_token: str, db: Session) -> str:
		"""Validate refresh token and issue a new access token."""
		try:
			payload = decode_jwt_token(refresh_token)
		except jwt.InvalidTokenError as exc:
			raise ValueError("Invalid refresh token") from exc

		if not is_refresh_token(payload):
			raise ValueError("Invalid refresh token")

		user_id = payload.get("sub")
		if not user_id:
			raise ValueError("Invalid refresh token")

		user = UserRepository(db).get_by_id(user_id)
		if not user:
			raise ValueError("Invalid refresh token")

		return create_access_token(user_id)

