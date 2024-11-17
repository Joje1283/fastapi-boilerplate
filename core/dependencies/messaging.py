from celery import Celery
from core.config import get_settings

settings = get_settings()

celery = Celery(
    "fastapi-sc",
    broker=settings.celery_broker_url,
    backend=settings.celery_backend_url,
    broker_connection_retry_on_startup=True,
)
