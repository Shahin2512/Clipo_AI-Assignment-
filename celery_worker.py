from celery import Celery
from app.config import settings

celery_app = Celery(
    "worker",
    broker=settings.REDIS_BROKER
)

celery_app.conf.task_routes = {
    "app.tasks.process_video": {"queue": "video"}
}
