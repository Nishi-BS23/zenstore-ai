from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.models.user import User


router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict[str, str]:
	return {"status": "ok"}


@router.get("/protected")
def protected_endpoint(current_user: User = Depends(get_current_user)) -> dict:
	"""Protected endpoint that requires authentication."""
	return {
		"message": "This is a protected endpoint",
		"user_id": current_user.id,
		"user_email": current_user.email,
	}

