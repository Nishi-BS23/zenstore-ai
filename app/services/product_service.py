from sqlalchemy.orm import Session

from app.models.product import Product, ProductStatus
from app.models.user import User
from app.repositories.product_repository import ProductRepository
from app.utils.decorators import performance_logger


class ProductService:
	"""Service for product operations with owner-based access control."""

	@staticmethod
	@performance_logger
	def create_product(
		name: str,
		price: float,
		details: str,
		owner: User,
		db: Session,
		description: str | None = None,
		category: str | None = None,
		status: ProductStatus = ProductStatus.pending,
	) -> Product:
		"""Create a product for the authenticated user."""
		repo = ProductRepository(db)
		return repo.create(
			name=name,
			price=price,
			details=details,
			owner=owner,
			description=description,
			category=category,
			status=status,
		)

	@staticmethod
	@performance_logger
	def get_product_by_id(product_id: str, owner: User, db: Session) -> Product | None:
		"""Get product by ID only if owner matches."""
		repo = ProductRepository(db)
		return repo.get_by_id(product_id, owner)

	@staticmethod
	@performance_logger
	def list_products(owner: User, db: Session, skip: int = 0, limit: int = 100) -> list[Product]:
		"""List all products for the authenticated user."""
		repo = ProductRepository(db)
		return repo.list_by_owner(owner, skip=skip, limit=limit)

	@staticmethod
	@performance_logger
	def update_product(
		product_id: str,
		owner: User,
		db: Session,
		name: str | None = None,
		price: float | None = None,
		details: str | None = None,
		description: str | None = None,
		category: str | None = None,
		status: ProductStatus | None = None,
	) -> Product | None:
		"""Update product only if owner matches."""
		repo = ProductRepository(db)
		product = repo.get_by_id(product_id, owner)

		if not product:
			return None

		return repo.update(
			product,
			name=name,
			price=price,
			details=details,
			description=description,
			category=category,
			status=status,
		)

	@staticmethod
	@performance_logger
	def delete_product(product_id: str, owner: User, db: Session) -> bool:
		"""Delete product only if owner matches."""
		repo = ProductRepository(db)
		product = repo.get_by_id(product_id, owner)

		if not product:
			return False

		repo.delete(product)
		return True

