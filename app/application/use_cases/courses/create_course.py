from dataclasses import dataclass
from uuid import uuid4

from app.application.interfaces.repositories.course_repository import CourseRepository
from app.domain.entities.course import Course


@dataclass(slots=True)
class CreateCourseCommand:
    title: str
    description: str


class CreateCourseUseCase:
    def __init__(self, course_repository: CourseRepository) -> None:
        self.course_repository = course_repository

    async def execute(self, command: CreateCourseCommand) -> Course:
        course = Course(
            id=uuid4(),
            title=command.title,
            description=command.description,
        )
        await self.course_repository.add(course)
        return course
