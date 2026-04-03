import re

from pydantic import BaseModel, EmailStr, Field, field_validator


PASSWORD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z\d]).+$")


class RegisterRequest(BaseModel):
	email: EmailStr
	password: str = Field(..., min_length=8)

	@field_validator("password")
	@classmethod
	def validate_password_strength(cls, value: str) -> str:
		"""Require strong passwords for account registration."""
		if not PASSWORD_REGEX.match(value):
			raise ValueError(
				"Password must include uppercase, lowercase, number, and special character"
			)
		return value


class LoginRequest(BaseModel):
	email: EmailStr
	password: str


class RefreshTokenRequest(BaseModel):
	refresh_token: str


class TokenResponse(BaseModel):
	access_token: str
	refresh_token: str
	token_type: str = "bearer"


class UserResponse(BaseModel):
	id: str
	email: str

	class Config:
		from_attributes = True

