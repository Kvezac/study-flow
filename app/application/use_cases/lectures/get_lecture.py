from dataclasses import dataclass
from uuid import UUID

from app.application.exceptions import LectureNotFoundError
from app.application.interfaces.repositories.lecture_repository import LectureRepository
from app.domain.entities.lecture import Lecture


@dataclass(slots=True)
class GetLectureQuery:
    lecture_id: UUID


class GetLectureUseCase:
    def __init__(self, lecture_repository: LectureRepository) -> None:
        self.lecture_repository = lecture_repository

    async def execute(self, query: GetLectureQuery) -> Lecture:
        lecture = await self.lecture_repository.get_by_id(query.lecture_id)
        if lecture is None:
            raise LectureNotFoundError("Lecture not found.")
        return lecture
