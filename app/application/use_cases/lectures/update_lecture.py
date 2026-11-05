from dataclasses import dataclass
from uuid import UUID

from app.application.exceptions import LectureNotFoundError
from app.application.interfaces.unit_of_work import UnitOfWork
from app.domain.entities.lecture import Lecture


@dataclass(slots=True)
class UpdateLectureCommand:
    lecture_id: UUID
    title: str
    content: str
    position: int


class UpdateLectureUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def execute(self, command: UpdateLectureCommand) -> Lecture:
        async with self.uow:
            lecture = await self.uow.lectures.get_by_id(command.lecture_id)
            if lecture is None:
                raise LectureNotFoundError("Lecture not found.")

            lecture.update(
                title=command.title,
                content=command.content,
                position=command.position,
            )
            await self.uow.lectures.update(lecture)
            await self.uow.commit()
            return lecture
