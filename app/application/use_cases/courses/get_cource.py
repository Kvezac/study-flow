from dataclasses import dataclass
from uuid import UUID

from app.application.exceptions import CourseNotFoundError
from app.application.interfaces.repositories.course_repository import CourseRepository
from app.domain.entities import Course


@dataclass(slots=True)
class GetCourseQuery:
    course_id: UUID


class GetCourseUseCase:
    def __init__(self, course_repository: CourseRepository) -> None:
        self.course_repository = course_repository

    async def execute(self, query: GetCourseQuery) -> Course:
        course = await self.course_repository.get_by_id(query.course_id)
        if course is None:
            raise CourseNotFoundError("Course not found.")
        return course
