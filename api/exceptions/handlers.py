from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from .database_exception import DatabaseException
from .domain_exception import DomainException
from .resource_not_found_exception import ResourceNotFoundException


def format_error_response(status_code: int, message: str, error_code: str | None = None):
    content = {"detail": message}

    if error_code:
        content["error_code"] = error_code

    return JSONResponse(status_code=status_code, content=content)

def register_exception_handlers(app: FastAPI):

    @app.exception_handler(ResourceNotFoundException)
    async def resource_not_found_handler(req: Request, exc: ResourceNotFoundException):
        return format_error_response(
            status_code=status.HTTP_404_NOT_FOUND,
            message=str(exc),
            error_code="RESOURCE_NOT_FOUND",
        )

    @app.exception_handler(DatabaseException)
    async def database_exception_handler(req: Request, exc: DatabaseException):
        return format_error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=str(exc),
            error_code="DATABASE_ERROR",
        )

    @app.exception_handler(DomainException)
    async def domain_exception_handler(req: Request, exc: DomainException):
        return format_error_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=str(exc),
            error_code="DOMAIN_ERROR",
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(req: Request, exc: Exception):
        return format_error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="An unexpected internal server error occurred.",
            error_code="INTERNAL_SERVER_ERROR",
        )
