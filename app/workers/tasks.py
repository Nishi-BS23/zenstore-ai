from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.product import Product, ProductStatus
from app.models.user import User  # noqa: F401
from app.services.cache_service import CacheService
from app.services.ai_service import AIService
from app.workers.celery_app import celery_app


def _fallback_content(product: Product) -> dict[str, str]:
	"""Fallback content when AI generation fails."""
	return AIService.default_content_from_name(product.name)


@celery_app.task(name="generate_ai_content")
def generate_ai_content(product_id: str) -> dict[str, str]:
	"""Fetch a product, generate AI content, and persist results asynchronously."""
	cache_service = CacheService()
	db: Session = SessionLocal()
	try:
		product = db.query(Product).filter(Product.id == product_id).first()
		if not product:
			return {"status": "missing", "product_id": product_id}

		try:
			content = AIService.generate(product)
			product.description = content["description"]
			product.category = content["category"]
			product.status = ProductStatus.done
		except Exception:
			content = _fallback_content(product)
			product.description = content["description"]
			product.category = content["category"]
			product.status = ProductStatus.failed

		db.commit()
		db.refresh(product)
		cache_service.invalidate_product(product.id)
		return {
			"status": product.status.value,
			"product_id": product.id,
			"description": product.description or "",
			"category": product.category or "",
		}
	finally:
		db.close()

