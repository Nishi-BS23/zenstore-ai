from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.services.product_service import ProductService
from app.workers.tasks import generate_ai_content


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/products", tags=["products"])


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(
	product_in: ProductCreate,
	current_user: User = Depends(get_current_user),
	db: Session = Depends(get_db),
):
	"""Create a new product."""
	product = ProductService.create_product(
		name=product_in.name,
		price=product_in.price,
		details=product_in.details,
		owner=current_user,
		db=db,
		description=product_in.description,
		category=product_in.category,
	)
	try:
		generate_ai_content.delay(product.id)
	except Exception as exc:  # noqa: BLE001 - background dispatch must not fail the API
		logger.warning("Failed to enqueue generate_ai_content for product %s: %s", product.id, exc)
	return product


@router.get("/{product_id}", response_model=ProductRead)
def get_product(
	product_id: str,
	current_user: User = Depends(get_current_user),
	db: Session = Depends(get_db),
):
	"""Get a product by ID."""
	product = ProductService.get_product_by_id(product_id, current_user, db)
	if not product:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Product not found",
		)
	return product


@router.get("", response_model=list[ProductRead])
def list_products(
	skip: int = 0,
	limit: int = 100,
	current_user: User = Depends(get_current_user),
	db: Session = Depends(get_db),
):
	"""List all products for the current user."""
	products = ProductService.list_products(current_user, db, skip, limit)
	return products


@router.put("/{product_id}", response_model=ProductRead)
def update_product(
	product_id: str,
	product_in: ProductUpdate,
	current_user: User = Depends(get_current_user),
	db: Session = Depends(get_db),
):
	"""Update a product."""
	product = ProductService.update_product(
		product_id=product_id,
		owner=current_user,
		db=db,
		name=product_in.name,
		price=product_in.price,
		details=product_in.details,
		description=product_in.description,
		category=product_in.category,
		status=product_in.status,
	)
	if not product:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Product not found",
		)
	return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
	product_id: str,
	current_user: User = Depends(get_current_user),
	db: Session = Depends(get_db),
):
	"""Delete a product."""
	success = ProductService.delete_product(product_id, current_user, db)
	if not success:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Product not found",
		)
	return None

