class DatabaseOperationException(Exception):
    """Raised for errors during database operations"""
    def __init__(self, message: str):
        super().__init__(message)