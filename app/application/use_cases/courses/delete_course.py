from dataclasses import dataclass
from uuid import UUID

from app.application.exceptions import CourseNotFoundError
from app.application.interfaces.unit_of_work import UnitOfWork
from app.domain.entities.module import Module
from app.domain.entities.section import Section


@dataclass(slots=True)
class DeleteCourseCommand:
    course_id: UUID


class DeleteCourseUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def execute(self, command: DeleteCourseCommand) -> None:
        async with self.uow:
            course = await self.uow.courses.get_by_id(command.course_id)
            if course is None:
                raise CourseNotFoundError("Course not found.")

            modules = await self.uow.modules.get_by_ids(course.module_ids)
            section_ids = self._collect_section_ids(modules)
            sections = await self.uow.sections.get_by_ids(section_ids)
            lecture_ids = self._collect_lecture_ids(sections)

            await self.uow.lectures.remove(lecture_ids)
            await self.uow.sections.remove(section_ids)
            await self.uow.modules.remove(course.module_ids)
            await self.uow.courses.remove(command.course_id)
            await self.uow.commit()

    def _collect_section_ids(self, modules: list[Module]) -> list[UUID]:
        section_ids: list[UUID] = []
        for module in modules:
            section_ids.extend(module.section_ids)
        return section_ids

    def _collect_lecture_ids(self, sections: list[Section]) -> list[UUID]:
        lecture_ids: list[UUID] = []
        for section in sections:
            lecture_ids.extend(section.lecture_ids)
        return lecture_ids
