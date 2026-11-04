from dataclasses import dataclass
from uuid import UUID

from app.application.exceptions import CourseNotFoundError
from app.application.interfaces.repositories.course_repository import CourseRepository
from app.domain.entities.course import Course


@dataclass(slots=True)
class UpdateCourseCommand:
    course_id: UUID
    title: str
    description: str


class UpdateCourseUseCase:
    def __init__(self, course_repository: CourseRepository) -> None:
        self.course_repository = course_repository

    async def execute(self, command: UpdateCourseCommand) -> Course:
        course = await self.course_repository.get_by_id(command.course_id)
        if course is None:
            raise CourseNotFoundError("Course not found.")

        course.update(
            title=command.title,
            description=command.description,
        )
        await self.course_repository.update(course)
        return course
