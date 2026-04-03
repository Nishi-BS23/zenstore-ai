from sqlalchemy.orm import Session

from app.core.security import create_jwt_token, hash_password, verify_password
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
	def login_user(email: str, password: str, db: Session) -> tuple[User, str]:
		"""Authenticate user and return user + JWT token."""
		repo = UserRepository(db)
		user = repo.get_by_email(email)
		if not user:
			raise ValueError("Invalid email or password")

		if not verify_password(password, user.hashed_password):
			raise ValueError("Invalid email or password")

		token = create_jwt_token(user.id)
		return user, token

