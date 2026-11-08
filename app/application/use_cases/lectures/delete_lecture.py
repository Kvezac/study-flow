from dataclasses import dataclass
from uuid import UUID

from app.application.exceptions import LectureNotFoundError, SectionNotFoundError
from app.application.interfaces.unit_of_work import UnitOfWork


@dataclass(slots=True)
class DeleteLectureCommand:
    lecture_id: UUID


class DeleteLectureUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def execute(self, command: DeleteLectureCommand) -> None:
        async with self.uow:
            lecture = await self.uow.lectures.get_by_id(command.lecture_id)
            if lecture is None:
                raise LectureNotFoundError("Lecture not found.")

            section = await self.uow.sections.get_by_id(lecture.section_id)
            if section is None:
                raise SectionNotFoundError("Section not found.")

            await self.uow.lectures.remove([command.lecture_id])
            section.remove_lecture(command.lecture_id)
            await self.uow.sections.update(section)
            await self.uow.commit()
