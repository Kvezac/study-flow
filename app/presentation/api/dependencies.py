from collections.abc import AsyncIterator

from fastapi import Depends

from app.application.use_cases.courses.create_course import CreateCourseUseCase
from app.application.use_cases.courses.get_course import GetCourseUseCase
from app.application.use_cases.courses.get_course_structure import (
    GetCourseStructureUseCase,
)
from app.application.use_cases.courses.get_courses import GetCoursesUseCase
from app.application.use_cases.courses.update_course import UpdateCourseUseCase
from app.application.use_cases.lectures.create_lecture import CreateLectureUseCase
from app.application.use_cases.lectures.get_lecture import GetLectureUseCase
from app.application.use_cases.lectures.update_lecture import UpdateLectureUseCase
from app.application.use_cases.modules.create_module import CreateModuleUseCase
from app.application.use_cases.modules.update_module import UpdateModuleUseCase
from app.application.use_cases.sections.create_section import CreateSectionUseCase
from app.application.use_cases.sections.update_section import UpdateSectionUseCase
from app.infrastructure.database import SessionFactory, SqlAlchemyUnitOfWork


async def get_uow() -> AsyncIterator[SqlAlchemyUnitOfWork]:
    async with SqlAlchemyUnitOfWork(session_factory=SessionFactory) as uow:
        yield uow


def get_get_courses_use_case(
    uow: SqlAlchemyUnitOfWork = Depends(get_uow),
) -> GetCoursesUseCase:
    return GetCoursesUseCase(course_repository=uow.courses)


def get_get_course_use_case(
    uow: SqlAlchemyUnitOfWork = Depends(get_uow),
) -> GetCourseUseCase:
    return GetCourseUseCase(course_repository=uow.courses)


def get_get_course_structure_use_case(
    uow: SqlAlchemyUnitOfWork = Depends(get_uow),
) -> GetCourseStructureUseCase:
    return GetCourseStructureUseCase(
        course_repository=uow.courses,
        module_repository=uow.modules,
        section_repository=uow.sections,
        lecture_repository=uow.lectures,
    )


def get_get_lecture_use_case(
    uow: SqlAlchemyUnitOfWork = Depends(get_uow),
) -> GetLectureUseCase:
    return GetLectureUseCase(lecture_repository=uow.lectures)


def get_create_course_use_case() -> CreateCourseUseCase:
    return CreateCourseUseCase(uow=SqlAlchemyUnitOfWork(session_factory=SessionFactory))


def get_update_course_use_case() -> UpdateCourseUseCase:
    return UpdateCourseUseCase(uow=SqlAlchemyUnitOfWork(session_factory=SessionFactory))


def get_create_module_use_case() -> CreateModuleUseCase:
    return CreateModuleUseCase(uow=SqlAlchemyUnitOfWork(session_factory=SessionFactory))


def get_update_module_use_case() -> UpdateModuleUseCase:
    return UpdateModuleUseCase(uow=SqlAlchemyUnitOfWork(session_factory=SessionFactory))


def get_create_section_use_case() -> CreateSectionUseCase:
    return CreateSectionUseCase(
        uow=SqlAlchemyUnitOfWork(session_factory=SessionFactory)
    )


def get_update_section_use_case() -> UpdateSectionUseCase:
    return UpdateSectionUseCase(
        uow=SqlAlchemyUnitOfWork(session_factory=SessionFactory)
    )


def get_create_lecture_use_case() -> CreateLectureUseCase:
    return CreateLectureUseCase(
        uow=SqlAlchemyUnitOfWork(session_factory=SessionFactory)
    )


def get_update_lecture_use_case() -> UpdateLectureUseCase:
    return UpdateLectureUseCase(
        uow=SqlAlchemyUnitOfWork(session_factory=SessionFactory)
    )
