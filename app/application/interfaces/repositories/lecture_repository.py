from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.lecture import Lecture


class LectureRepository(ABC):
    @abstractmethod
    async def get_by_id(self, lecture_id: UUID) -> Lecture | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_ids(self, lecture_ids: list[UUID]) -> list[Lecture]:
        raise NotImplementedError

    @abstractmethod
    async def add(self, lecture: Lecture) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, lecture: Lecture) -> None:
        raise NotImplementedError
