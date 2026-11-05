from dataclasses import dataclass
from uuid import UUID, uuid4

from app.application.exceptions import CourseNotFoundError
from app.application.interfaces.unit_of_work import UnitOfWork
from app.domain.entities.module import Module


@dataclass(slots=True)
class CreateModuleCommand:
    course_id: UUID
    title: str
    description: str
    position: int


class CreateModuleUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def execute(self, command: CreateModuleCommand) -> Module:
        async with self.uow:
            course = await self.uow.courses.get_by_id(command.course_id)
            if course is None:
                raise CourseNotFoundError("Course not found.")

            module = Module(
                id=uuid4(),
                course_id=command.course_id,
                title=command.title,
                description=command.description,
                position=command.position,
            )
            course.add_module(module.id)
            await self.uow.modules.add(module)
            await self.uow.courses.update(course)
            await self.uow.commit()
            return module
