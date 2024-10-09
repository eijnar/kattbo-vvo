from logging import getLogger
from celery import Celery
from core.config import settings

logger = getLogger(__name__)

def make_celery(app_name=__name__):
    broker_url = f'amqp://{settings.RABBITMQ_USERNAME}:{settings.RABBITMQ_PASSWORD}@{settings.RABBITMQ_HOSTNAME}:{settings.RABBITMQ_PORT}/{settings.RABBITMQ_VHOST}'
    backend_url = f'redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOSTNAME}:{settings.REDIS_PORT}/{settings.REDIS_CELERY_DB}'

    celery_app = Celery(
        app_name,
        broker=broker_url,
        backend=backend_url,
    )

    celery_app.conf.update(
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        enable_utc=True,
        result_expires=3600,
        task_acks_late=True,
        worker_prefetch_multiplier=1,
        imports=['core.tasks']
    )

    celery_app.autodiscover_tasks(['core.tasks.notification_task'])
    
    return celery_app

celery_app = make_celery()