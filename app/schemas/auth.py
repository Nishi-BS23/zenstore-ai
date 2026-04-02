from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
	email: str = Field(..., min_length=1, max_length=255)
	password: str = Field(..., min_length=8)


class LoginRequest(BaseModel):
	email: str
	password: str


class TokenResponse(BaseModel):
	access_token: str
	token_type: str = "bearer"


class UserResponse(BaseModel):
	id: str
	email: str

	class Config:
		from_attributes = True

