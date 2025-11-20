import logging
import traceback
from typing import Callable, TypeVar

from fastapi import HTTPException, status

from app.utils.exception_handler import CustomException, ExceptionType

logger = logging.getLogger("app")

T = TypeVar("T")


def log_operation_start(operation: str) -> None:
    logger.info("Starting operation: %s", operation)


def log_operation_success(operation: str) -> None:
    logger.info("Completed operation: %s", operation)


def raise_http_exception(operation: str, exc: Exception) -> None:
    stack_trace = traceback.format_exc()
    logger.error("Operation %s failed: %s\n%s", operation, exc, stack_trace)

    if isinstance(exc, HTTPException):
        raise exc

    if isinstance(exc, CustomException):
        status_code = exc.http_code or ExceptionType.INTERNAL_SERVER_ERROR.http_code
        detail = exc.message or ExceptionType.INTERNAL_SERVER_ERROR.message
        raise HTTPException(status_code=status_code, detail=detail)

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=ExceptionType.INTERNAL_SERVER_ERROR.message,
    )


def execute_with_logging(operation: str, func: Callable[[], T]) -> T:
    log_operation_start(operation)
    try:
        result = func()
        log_operation_success(operation)
        return result
    except Exception as exc:
        raise_http_exception(operation, exc)

