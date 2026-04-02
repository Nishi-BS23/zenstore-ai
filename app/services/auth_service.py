from sqlalchemy.orm import Session

from app.core.security import create_jwt_token, hash_password, verify_password
from app.models.user import User


class AuthService:
	"""Service for authentication operations."""

	@staticmethod
	def register_user(email: str, password: str, db: Session) -> User:
		"""Register a new user."""
		existing = db.query(User).filter(User.email == email).first()
		if existing:
			raise ValueError(f"User with email {email} already exists")

		hashed_pwd = hash_password(password)
		new_user = User(email=email, hashed_password=hashed_pwd)
		db.add(new_user)
		db.commit()
		db.refresh(new_user)
		return new_user

	@staticmethod
	def login_user(email: str, password: str, db: Session) -> tuple[User, str]:
		"""Authenticate user and return user + JWT token."""
		user = db.query(User).filter(User.email == email).first()
		if not user:
			raise ValueError("Invalid email or password")

		if not verify_password(password, user.hashed_password):
			raise ValueError("Invalid email or password")

		token = create_jwt_token(user.id)
		return user, token

