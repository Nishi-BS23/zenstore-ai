from sqlalchemy.orm import Session

from app.models.product import Product, ProductStatus
from app.models.user import User


class ProductRepository:
	"""Database access for product records."""

	def __init__(self, db: Session) -> None:
		self.db = db

	def create(
		self,
		name: str,
		price: float,
		details: str,
		owner: User,
		description: str | None = None,
		category: str | None = None,
		status: ProductStatus = ProductStatus.pending,
	) -> Product:
		product = Product(
			name=name,
			price=price,
			details=details,
			description=description,
			category=category,
			status=status,
			owner_id=owner.id,
		)
		self.db.add(product)
		self.db.commit()
		self.db.refresh(product)
		return product

	def get_by_id(self, product_id: str, owner: User) -> Product | None:
		return self.db.query(Product).filter(
			Product.id == product_id,
			Product.owner_id == owner.id,
		).first()

	def get_by_id_any_owner(self, product_id: str) -> Product | None:
		return self.db.query(Product).filter(Product.id == product_id).first()

	def list_by_owner(self, owner: User, skip: int = 0, limit: int = 100) -> list[Product]:
		return self.db.query(Product).filter(
			Product.owner_id == owner.id,
		).offset(skip).limit(limit).all()

	def update(
		self,
		product: Product,
		name: str | None = None,
		price: float | None = None,
		details: str | None = None,
		description: str | None = None,
		category: str | None = None,
		status: ProductStatus | None = None,
	) -> Product:
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

		self.db.commit()
		self.db.refresh(product)
		return product

	def delete(self, product: Product) -> None:
		self.db.delete(product)
		self.db.commit()
