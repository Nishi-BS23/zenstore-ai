from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.auth import (
	LoginRequest,
	RefreshTokenRequest,
	RegisterRequest,
	TokenResponse,
	UserResponse,
)
from app.services.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(req: RegisterRequest, db: Session = Depends(get_db)) -> User:
	"""Register a new user."""
	try:
		user = AuthService.register_user(req.email, req.password, db)
		return user
	except ValueError as e:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)) -> dict:
	"""Login user and return JWT token."""
	try:
		user, access_token, refresh_token = AuthService.login_user(req.email, req.password, db)
		return {
			"access_token": access_token,
			"refresh_token": refresh_token,
			"token_type": "bearer",
		}
	except ValueError as e:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/refresh", response_model=TokenResponse)
def refresh(req: RefreshTokenRequest, db: Session = Depends(get_db)) -> dict:
	"""Refresh access token using a valid refresh token."""
	try:
		access_token = AuthService.refresh_access_token(req.refresh_token, db)
		return {
			"access_token": access_token,
			"refresh_token": req.refresh_token,
			"token_type": "bearer",
		}
	except ValueError as e:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)) -> User:
	"""Get current authenticated user info."""
	return current_user

