from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from app.application.use_cases.courses.get_course import (
    GetCourseQuery,
    GetCourseUseCase,
)
from app.application.use_cases.courses.get_course_structure import (
    GetCourseStructureQuery,
    GetCourseStructureUseCase,
)
from app.application.use_cases.courses.get_courses import (
    GetCoursesQuery,
    GetCoursesUseCase,
)
from app.application.use_cases.lectures.get_lecture import (
    GetLectureQuery,
    GetLectureUseCase,
)
from app.presentation.api.dependencies import (
    get_get_course_structure_use_case,
    get_get_course_use_case,
    get_get_courses_use_case,
    get_get_lecture_use_case,
)
from app.presentation.api.schemas import (
    CourseListItemResponse,
    CourseResponse,
    CourseStructureResponse,
    ErrorResponse,
    LectureResponse,
)

router = APIRouter(tags=["Content"])


@router.get(
    "/courses",
    response_model=list[CourseListItemResponse],
    summary="List available courses",
    description="Returns a public list of courses available in the system.",
)
async def get_courses(
    use_case: Annotated[GetCoursesUseCase, Depends(get_get_courses_use_case)],
) -> list[CourseListItemResponse]:
    result = await use_case.execute(GetCoursesQuery())
    return [CourseListItemResponse.model_validate(course) for course in result]


@router.get(
    "/courses/{course_id}",
    response_model=CourseResponse,
    summary="Get course by ID",
    description="Returns a single course by its identifier.",
    responses={
        404: {
            "description": "Course was not found.",
            "model": ErrorResponse,
        },
    },
)
async def get_course(
    course_id: UUID,
    use_case: Annotated[GetCourseUseCase, Depends(get_get_course_use_case)],
) -> CourseResponse:
    result = await use_case.execute(GetCourseQuery(course_id=course_id))
    return CourseResponse.model_validate(result)


@router.get(
    "/courses/{course_id}/structure",
    response_model=CourseStructureResponse,
    summary="Get course structure",
    description=(
        "Returns the course navigation tree: modules, sections and lectures "
        "without full lecture content."
    ),
    responses={
        404: {
            "description": "Course was not found.",
            "model": ErrorResponse,
        },
    },
)
async def get_course_structure(
    course_id: UUID,
    use_case: Annotated[GetCourseStructureUseCase, Depends(get_get_course_structure_use_case)],
) -> CourseStructureResponse:
    result = await use_case.execute(GetCourseStructureQuery(course_id=course_id))
    return CourseStructureResponse.model_validate(result)


@router.get(
    "/lectures/{lecture_id}",
    response_model=LectureResponse,
    summary="Get lecture by ID",
    description="Returns the full content of a single lecture.",
    responses={
        404: {
            "description": "Lecture was not found.",
            "model": ErrorResponse,
        },
    },
)
async def get_lecture(
    lecture_id: UUID,
    use_case: Annotated[GetLectureUseCase, Depends(get_get_lecture_use_case)],
) -> LectureResponse:
    result = await use_case.execute(GetLectureQuery(lecture_id=lecture_id))
    return LectureResponse.model_validate(result)
