from dataclasses import dataclass

from app.application.interfaces.repositories.course_repository import CourseRepository
from app.domain.entities.course import Course


@dataclass(slots=True)
class GetCoursesQuery:
    pass


class GetCoursesUseCase:
    def __init__(self, course_repository: CourseRepository) -> None:
        self.course_repository = course_repository

    async def execute(self, query: GetCoursesQuery) -> list[Course]:
        return await self.course_repository.list()
