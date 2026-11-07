from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.application.exceptions import (
    ApplicationError,
    CourseNotFoundError,
    LectureNotFoundError,
    ModuleNotFoundError,
    SectionNotFoundError,
)
from app.domain.exceptions import DomainError
from app.presentation.api.schemas import ErrorResponse


def build_error_response(error: str, message: str, status_code: int) -> JSONResponse:
    payload = ErrorResponse(error=error, message=message)
    return JSONResponse(status_code=status_code, content=payload.model_dump())


async def domain_error_handler(request: Request, exc: Exception) -> JSONResponse:
    return build_error_response(
        error="domain_error",
        message=str(exc),
        status_code=status.HTTP_400_BAD_REQUEST,
    )


async def application_error_handler(request: Request, exc: Exception) -> JSONResponse:
    return build_error_response(
        error="application_error",
        message=str(exc),
        status_code=status.HTTP_400_BAD_REQUEST,
    )


async def course_not_found_handler(request: Request, exc: Exception) -> JSONResponse:
    return build_error_response(
        error="course_not_found",
        message=str(exc),
        status_code=status.HTTP_404_NOT_FOUND,
    )


async def module_not_found_handler(request: Request, exc: Exception) -> JSONResponse:
    return build_error_response(
        error="module_not_found",
        message=str(exc),
        status_code=status.HTTP_404_NOT_FOUND,
    )


async def section_not_found_handler(request: Request, exc: Exception) -> JSONResponse:
    return build_error_response(
        error="section_not_found",
        message=str(exc),
        status_code=status.HTTP_404_NOT_FOUND,
    )


async def lecture_not_found_handler(request: Request, exc: Exception) -> JSONResponse:
    return build_error_response(
        error="lecture_not_found",
        message=str(exc),
        status_code=status.HTTP_404_NOT_FOUND,
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(DomainError, domain_error_handler)
    app.add_exception_handler(ApplicationError, application_error_handler)
    app.add_exception_handler(CourseNotFoundError, course_not_found_handler)
    app.add_exception_handler(ModuleNotFoundError, module_not_found_handler)
    app.add_exception_handler(SectionNotFoundError, section_not_found_handler)
    app.add_exception_handler(LectureNotFoundError, lecture_not_found_handler)
