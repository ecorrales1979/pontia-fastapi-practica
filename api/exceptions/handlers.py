import traceback
from typing import NamedTuple

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from api.utils import Logger

from .business_exception import BusinessException
from .database_exception import DatabaseException
from .domain_exception import DomainException
from .resource_not_found_exception import ResourceNotFoundException

logger = Logger()


class ExceptionConfig(NamedTuple):
    status_code: int
    log_method: callable
    error_code: str | None = None
    include_trace: bool = False

CUSTOM_ESCEPTIONS: dict[type[Exception], ExceptionConfig] = {
    ResourceNotFoundException: ExceptionConfig(
        status_code=status.HTTP_404_NOT_FOUND,
        error_code="RESOURCE_NOT_FOUND",
        log_method=logger.warning,
    ),
    BusinessException: ExceptionConfig(
        status_code=status.HTTP_409_CONFLICT,
        error_code="BUSINESS_ERROR",
        log_method=logger.warning,
    ),
    DatabaseException: ExceptionConfig(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code="DATABASE_ERROR",
        log_method=logger.error,
        include_trace=True,
    ),
    DomainException: ExceptionConfig(
        status_code=status.HTTP_400_BAD_REQUEST,
        error_code="DOMAIN_ERROR",
        log_method=logger.warning,
    ),
}


class ExceptionHandlers:

    @staticmethod
    def _format_error_response(status_code: int, message: str, error_code: str | None = None):
        content = {"detail": message}

        if error_code:
            content["error_code"] = error_code

        return JSONResponse(status_code=status_code, content=content)

    @staticmethod
    def _build_request_context(req: Request) -> dict[str, str]:
        return {
            "path": req.url.path,
            "method": req.method,
        }

    @staticmethod
    def _build_trace(exc: Exception) -> str:
        return "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))

    @classmethod
    def _create_handler(cls, config: ExceptionConfig):
        async def handler(req: Request, exc: Exception) -> JSONResponse:
            context = {
                **cls._build_request_context(req),
                "error_code": config.error_code,
                "exception_type": type(exc).__name__,
            }

            log_payload = {
                "message":str(exc),
                "context":context,
            }
            if config.include_trace:
                log_payload["trace"] = cls._build_trace(exc)

            config.log_method(**log_payload)

            return cls._format_error_response(
                status_code=config.status_code,
                message=str(exc),
                error_code=config.error_code,
            )

        return handler

    @classmethod
    def register(cls, app: FastAPI):

        for exc_class, config in CUSTOM_ESCEPTIONS.items():
            handler = cls._create_handler(config)
            app.add_exception_handler(exc_class, handler)

        @app.exception_handler(Exception)
        async def unhandled_exception_handler(req: Request, exc: Exception):
            logger.critical(
                message="Unhandled exception",
                trace=cls._build_trace(exc),
                context={
                    **cls._build_request_context(req),
                    "error_code": "INTERNAL_SERVER_ERROR",
                    "exception_type": type(exc).__name__,
                },
            )
            return cls._format_error_response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="An unexpected internal server error occurred.",
                error_code="INTERNAL_SERVER_ERROR",
            )
