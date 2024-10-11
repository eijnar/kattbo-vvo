from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from .exceptions import NotFoundException, ConflictException, DatabaseException

async def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

async def conflict_exception_handler(request: Request, exc: ConflictException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

async def database_exception_handler(request: Request, exc: DatabaseException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    # Optionally, you can log the exception details here
    return JSONResponse(
        status_code=500,
        content={"detail": "A database error occurred."},
    )

async def generic_exception_handler(request: Request, exc: Exception):
    # Optionally, log the exception details
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred."},
    )