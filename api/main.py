import logging

import elasticapm
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from elasticapm.contrib.starlette import ElasticAPM
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from core.celery import make_celery
from core.config import settings
from core.database.base import create_tables
from core.logger.setup import setup_logging, apm_client
from core.security.endpoints import security
from routers.users.base import users
from routers.notification.base import notification
from utils.rate_limiter import limiter
from core.security.redis_client import init_redis_pools


logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(title=settings.APP_NAME)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(
        ElasticAPM,
        client=apm_client
    )

    @app.get("/")
    def read_root():
        return {"message": "The API is running..."}

    # Routers
    app.include_router(users, prefix="/v1")
    app.include_router(security, prefix="/v1")
    app.include_router(notification, prefix="/v1")

    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    celery_app = make_celery(app)
    app.celery_app = celery_app

    @app.on_event("startup")
    async def startup_event():
        # Create database tables
        await create_tables()
        await init_redis_pools()

    return app


def main():
    app = create_app()
    import uvicorn
    uvicorn.run("main:create_app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
