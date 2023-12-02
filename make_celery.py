from celery import Celery
from app import create_app

def make_celery(app):
    celery = Celery(app.import_name)
    celery_config = app.config.get('CELERY')
    if celery_config:
        celery.conf.update(celery_config)
    return celery

flask_app = create_app()
celery_app = make_celery(flask_app)