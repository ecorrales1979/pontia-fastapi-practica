from .domain_exception import DomainException


class DatabaseException(DomainException):
    def __init__(self, message: str = "A database error occurred", original_exception: Exception | None = None):
        self.original_exception = original_exception
        super().__init__(message)
