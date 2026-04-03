from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.product import Product, ProductStatus
from app.models.user import User  # noqa: F401
from app.repositories.product_repository import ProductRepository
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
		repo = ProductRepository(db)
		product = repo.get_by_id_any_owner(product_id)
		if not product:
			return {"status": "missing", "product_id": product_id}

		try:
			content = AIService.generate(product)
			updated = repo.update(
				product,
				description=content["description"],
				category=content["category"],
				status=ProductStatus.done,
			)
		except Exception:
			content = _fallback_content(product)
			updated = repo.update(
				product,
				description=content["description"],
				category=content["category"],
				status=ProductStatus.failed,
			)

		cache_service.invalidate_product(updated.id)
		return {
			"status": updated.status.value,
			"product_id": updated.id,
			"description": updated.description or "",
			"category": updated.category or "",
		}
	finally:
		db.close()

