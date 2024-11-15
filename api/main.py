from logging import getLogger

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
#from core.redis.factory import init_redis_pools
from core.exceptions_handlers import (
    base_app_exception_handler,
    sqlalchemy_exception_handler,
    generic_exception_handler
)
from core.exceptions import BaseAppException


logger = getLogger(__name__)


def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(
        title=settings.APP_NAME,
        version="1.1"
        )

    app.add_middleware(LoggingMiddleware)

    allowed_origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173"
        "http://0.0.0.0"
    ]

    app.add_middleware(SessionMiddleware,
                       secret_key=settings.SESSION_SECRET_KEY)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
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

    # celery_app = make_celery(app)
    # app.celery_app = celery_app

    # @app.on_event("startup")
    # async def startup_event():
    #     # Create database tables
    #     await create_tables()
    #     await init_redis_pools()

    return app


def main():
    app = create_app()

    import uvicorn
    uvicorn.run("main:create_app", host="0.0.0.0",
                port=8000, reload=True, factory=True)


if __name__ == "__main__":
    main()
