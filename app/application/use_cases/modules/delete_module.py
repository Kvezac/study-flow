from dataclasses import dataclass
from uuid import UUID

from app.application.exceptions import CourseNotFoundError, ModuleNotFoundError
from app.application.interfaces.unit_of_work import UnitOfWork
from app.domain.entities.section import Section


@dataclass(slots=True)
class DeleteModuleCommand:
    module_id: UUID


class DeleteModuleUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def execute(self, command: DeleteModuleCommand) -> None:
        async with self.uow:
            module = await self.uow.modules.get_by_id(command.module_id)
            if module is None:
                raise ModuleNotFoundError("Module not found.")

            course = await self.uow.courses.get_by_id(module.course_id)
            if course is None:
                raise CourseNotFoundError("Course not found.")

            sections = await self.uow.sections.get_by_ids(module.section_ids)
            lecture_ids = self._collect_lecture_ids(sections)

            await self.uow.lectures.remove(lecture_ids)
            await self.uow.sections.remove(module.section_ids)
            await self.uow.modules.remove([command.module_id])
            course.remove_module(command.module_id)
            await self.uow.courses.update(course)
            await self.uow.commit()

    def _collect_lecture_ids(self, sections: list[Section]) -> list[UUID]:
        lecture_ids: list[UUID] = []
        for section in sections:
            lecture_ids.extend(section.lecture_ids)
        return lecture_ids
