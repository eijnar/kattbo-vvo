from app import create_app, celery_init_app

app = create_app()
celery = celery_init_app(app)