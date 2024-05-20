import logging

from functools import wraps
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger("__name__")


class DatabaseOperationException(Exception):
    """Custom exception for database operation failures."""

    def __init__(self, operation, original_exception):
        super().__init__(
            f"Database error during {operation}: {str(original_exception)}")
        self.operation = operation
        self.original_exception = original_exception


def sqlalchemy_error_handler(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            #logger.debug(f"Successful database operation from {func}")
            return await func(*args, **kwargs)
        except SQLAlchemyError as e:
            logger.error("SQLAlchemy error occurred",
                         function_name=func.__name__, error=str(e))
            raise DatabaseOperationException(func.__name__, e)
        except Exception as e:
            logger.error("Unexpected error occurred",
                         function_name=func.__name__, error=str(e))
            raise DatabaseOperationException(func.__name__, e)
    return wrapper
