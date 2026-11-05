from dataclasses import dataclass
from uuid import UUID, uuid4

from app.application.exceptions import SectionNotFoundError
from app.application.interfaces.unit_of_work import UnitOfWork
from app.domain.entities.lecture import Lecture


@dataclass(slots=True)
class CreateLectureCommand:
    section_id: UUID
    title: str
    content: str
    position: int


class CreateLectureUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def execute(self, command: CreateLectureCommand) -> Lecture:
        async with self.uow:
            section = await self.uow.sections.get_by_id(command.section_id)
            if section is None:
                raise SectionNotFoundError("Section not found.")

            lecture = Lecture(
                id=uuid4(),
                section_id=command.section_id,
                title=command.title,
                content=command.content,
                position=command.position,
            )
            section.add_lecture(lecture.id)
            await self.uow.lectures.add(lecture)
            await self.uow.sections.update(section)
            await self.uow.commit()
            return lecture
