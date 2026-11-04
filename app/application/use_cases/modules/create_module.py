from dataclasses import dataclass
from uuid import UUID, uuid4

from app.application.exceptions import CourseNotFoundError
from app.application.interfaces.repositories.course_repository import CourseRepository
from app.application.interfaces.repositories.module_repository import ModuleRepository
from app.domain.entities.module import Module


@dataclass(slots=True)
class CreateModuleCommand:
    course_id: UUID
    title: str
    description: str
    position: int


class CreateModuleUseCase:
    def __init__(
        self,
        course_repository: CourseRepository,
        module_repository: ModuleRepository,
    ) -> None:
        self.course_repository = course_repository
        self.module_repository = module_repository

    async def execute(self, command: CreateModuleCommand) -> Module:
        course = await self.course_repository.get_by_id(command.course_id)
        if course is None:
            raise CourseNotFoundError("Course not found.")

        module = Module(
            id=uuid4(),
            course_id=course.id,
            title=command.title,
            description=command.description,
            position=command.position,
        )
        course.add_module(module.id)

        await self.module_repository.add(module)
        await self.course_repository.update(course)
        return module
