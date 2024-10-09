class ValidationException(Exception):
    """Raised for validation-related issues"""
    def __init__(self, message: str):
        super().__init__(message)