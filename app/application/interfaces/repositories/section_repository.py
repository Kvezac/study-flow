from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.section import Section


class SectionRepository(ABC):
    @abstractmethod
    async def get_by_id(self, section_id: UUID) -> Section | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_ids(self, section_ids: list[UUID]) -> list[Section]:
        raise NotImplementedError

    @abstractmethod
    async def add(self, section: Section) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, section: Section) -> None:
        raise NotImplementedError
