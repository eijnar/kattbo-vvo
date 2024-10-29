from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
import traceback

from .exceptions import BaseAppException
from logging import getLogger

logger = getLogger("app_logger")


async def base_app_exception_handler(request: Request, exc: BaseAppException):
    # Prepare log context with ECS fields and exception-specific extra context
    log_extra = {
        "client.address": request.client.host if request.client else "unknown",
        "url.path": request.url.path,
        "error.type": exc.__class__.__name__,
        "error.message": exc.detail,
        #"error.stack_trace": ''.join(traceback.format_exception(None, exc, exc.__traceback__)),
    }
    log_extra.update(exc.extra)  # Merge any additional context from the exception

    # Log the detailed error
    logger.error(
        exc.detail,
        extra=log_extra
    )
    
    # Return the user-facing error
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    log_extra = {
        "client.address": request.client.host if request.client else "unknown",
        "url.path": request.url.path,
        "error.type": exc.__class__.__name__,
        "error.message": str(exc),
        "error.stack_trace": ''.join(traceback.format_exception(None, exc, exc.__traceback__)),
    }

    logger.exception(
        f"SQLAlchemy error: {str(exc)}",
        extra=log_extra
    )
    
    return JSONResponse(
        status_code=500,
        content={"detail": "A database error occurred."},
    )

async def generic_exception_handler(request: Request, exc: Exception):
    log_extra = {
        "client.address": request.client.host if request.client else "unknown",
        "url.path": request.url.path,
        "error.type": exc.__class__.__name__,
        "error.message": str(exc),
        "error.stack_trace": ''.join(traceback.format_exception(None, exc, exc.__traceback__)),
    }

    logger.exception(
        f"Unhandled error: {str(exc)}",
        extra=log_extra
    )
    
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred."},
    )