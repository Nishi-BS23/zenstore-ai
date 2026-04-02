from celery import Celery

from app.core.config import settings


celery_app = Celery(
	"zenstore_ai",
	broker=settings.REDIS_URL,
	backend=settings.REDIS_URL,
	include=["app.workers.tasks"],
)

celery_app.conf.update(
	task_track_started=True,
	worker_prefetch_multiplier=1,
	task_acks_late=True,
	broker_connection_retry_on_startup=True,
)

