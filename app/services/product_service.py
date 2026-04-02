from sqlalchemy.orm import Session

from app.models.product import Product, ProductStatus
from app.models.user import User


class ProductService:
	"""Service for product operations with owner-based access control."""

	@staticmethod
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
		product = Product(
			name=name,
			price=price,
			details=details,
			description=description,
			category=category,
			status=status,
			owner_id=owner.id,
		)
		db.add(product)
		db.commit()
		db.refresh(product)
		return product

	@staticmethod
	def get_product_by_id(product_id: str, owner: User, db: Session) -> Product | None:
		"""Get product by ID only if owner matches."""
		product = db.query(Product).filter(
			Product.id == product_id,
			Product.owner_id == owner.id,
		).first()
		return product

	@staticmethod
	def list_products(owner: User, db: Session, skip: int = 0, limit: int = 100) -> list[Product]:
		"""List all products for the authenticated user."""
		products = db.query(Product).filter(
			Product.owner_id == owner.id,
		).offset(skip).limit(limit).all()
		return products

	@staticmethod
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
		product = db.query(Product).filter(
			Product.id == product_id,
			Product.owner_id == owner.id,
		).first()

		if not product:
			return None

		if name is not None:
			product.name = name
		if price is not None:
			product.price = price
		if details is not None:
			product.details = details
		if description is not None:
			product.description = description
		if category is not None:
			product.category = category
		if status is not None:
			product.status = status

		db.commit()
		db.refresh(product)
		return product

	@staticmethod
	def delete_product(product_id: str, owner: User, db: Session) -> bool:
		"""Delete product only if owner matches."""
		product = db.query(Product).filter(
			Product.id == product_id,
			Product.owner_id == owner.id,
		).first()

		if not product:
			return False

		db.delete(product)
		db.commit()
		return True

