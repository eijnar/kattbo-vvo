class BaseAppException(Exception):
    """Base class for application-specific exceptions."""
    status_code: int = 500
    detail: str = "An unexpected error occurred."
    extra: dict = {}

    def __init__(self, detail: str = None, extra: dict = None):
        if detail:
            self.detail = detail
        if extra:
            self.extra = extra


class NotFoundError(BaseAppException):
    status_code = 404
    detail = "Resource not found."


class ConflictError(BaseAppException):
    status_code = 409
    detail = "Conflict occurred."


class DatabaseError(BaseAppException):
    status_code = 500
    detail = "Database operation failed."


class ValidationError(BaseAppException):
    status_code = 400
    detail = "Validation failed."
