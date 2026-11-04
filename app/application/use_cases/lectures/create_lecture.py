from dataclasses import dataclass
from uuid import UUID, uuid4

from app.application.exceptions import SectionNotFoundError
from app.application.interfaces.repositories.lecture_repository import LectureRepository
from app.application.interfaces.repositories.section_repository import SectionRepository
from app.domain.entities.lecture import Lecture


@dataclass(slots=True)
class CreateLectureCommand:
    section_id: UUID
    title: str
    content: str
    position: int


class CreateLectureUseCase:
    def __init__(
        self,
        section_repository: SectionRepository,
        lecture_repository: LectureRepository,
    ) -> None:
        self.section_repository = section_repository
        self.lecture_repository = lecture_repository

    async def execute(self, command: CreateLectureCommand) -> Lecture:
        section = await self.section_repository.get_by_id(command.section_id)
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

        await self.lecture_repository.add(lecture)
        await self.section_repository.update(section)
        return lecture
