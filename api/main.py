from logging import getLogger
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from elasticapm.contrib.starlette import ElasticAPM
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.exc import SQLAlchemyError

from core.logger.middleware import LoggingMiddleware
# from core.celery import make_celery
from core.config import settings
from core.database.base import create_tables
from core.logger.setup import setup_logging, apm_client
from utils.rate_limiter import limiter
from core.redis.factory import init_redis_pools, redis_factory
from core.exceptions_handlers import (
    base_app_exception_handler,
    sqlalchemy_exception_handler,
    generic_exception_handler
)
from core.exceptions import BaseAppException


logger = getLogger(__name__)


def create_app() -> FastAPI:
    setup_logging()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Startup logic
        await init_redis_pools()
        yield
        # Shutdown logic
        await redis_factory.close_redis_pools()

    app = FastAPI(
        title=settings.APP_NAME,
        version="1.1",
        lifespan=lifespan
        )

    app.add_middleware(LoggingMiddleware)

    allowed_origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ]

    app.add_middleware(SessionMiddleware,
                       secret_key=settings.SESSION_SECRET_KEY)

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

    app.add_exception_handler(BaseAppException, base_app_exception_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)

    @app.get("/")
    def read_root():
        return {"message": "The API is running..."}

    from routers import api_router
    app.include_router(api_router, prefix="/v1")

    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


    return app

if __name__ == "__main__":
    print("This is meant to be run by a unicorn of uv light...")
