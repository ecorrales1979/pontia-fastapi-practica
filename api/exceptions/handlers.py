import traceback

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from api.utils import Logger

from .business_exception import BusinessException
from .database_exception import DatabaseException
from .domain_exception import DomainException
from .resource_not_found_exception import ResourceNotFoundException

logger = Logger()


def format_error_response(status_code: int, message: str, error_code: str | None = None):
    content = {"detail": message}

    if error_code:
        content["error_code"] = error_code

    return JSONResponse(status_code=status_code, content=content)


def _build_request_context(req: Request) -> dict[str, str]:
    return {
        "path": req.url.path,
        "method": req.method,
    }


def _build_trace(exc: Exception) -> str:
    return "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(ResourceNotFoundException)
    async def resource_not_found_handler(req: Request, exc: ResourceNotFoundException):
        logger.warning(
            message=str(exc),
            context={
                **_build_request_context(req),
                "error_code": "RESOURCE_NOT_FOUND",
                "exception_type": type(exc).__name__,
            },
        )
        return format_error_response(
            status_code=status.HTTP_404_NOT_FOUND,
            message=str(exc),
            error_code="RESOURCE_NOT_FOUND",
        )

    @app.exception_handler(BusinessException)
    async def business_exception_handler(req: Request, exc: BusinessException):
        logger.warning(
            message=str(exc),
            context={
                **_build_request_context(req),
                "error_code": "BUSINESS_ERROR",
                "exception_type": type(exc).__name__,
            },
        )
        return format_error_response(
            status_code=status.HTTP_409_CONFLICT,
            message=str(exc),
            error_code="BUSINESS_ERROR",
        )

    @app.exception_handler(DatabaseException)
    async def database_exception_handler(req: Request, exc: DatabaseException):
        logger.error(
            message=str(exc),
            trace=_build_trace(exc),
            context={
                **_build_request_context(req),
                "error_code": "DATABASE_ERROR",
                "exception_type": type(exc).__name__,
            },
        )
        return format_error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=str(exc),
            error_code="DATABASE_ERROR",
        )

    @app.exception_handler(DomainException)
    async def domain_exception_handler(req: Request, exc: DomainException):
        logger.warning(
            message=str(exc),
            context={
                **_build_request_context(req),
                "error_code": "DOMAIN_ERROR",
                "exception_type": type(exc).__name__,
            },
        )
        return format_error_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=str(exc),
            error_code="DOMAIN_ERROR",
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(req: Request, exc: Exception):
        logger.critical(
            message="Unhandled exception",
            trace=_build_trace(exc),
            context={
                **_build_request_context(req),
                "error_code": "INTERNAL_SERVER_ERROR",
                "exception_type": type(exc).__name__,
            },
        )
        return format_error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="An unexpected internal server error occurred.",
            error_code="INTERNAL_SERVER_ERROR",
        )
