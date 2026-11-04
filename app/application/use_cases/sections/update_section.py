from dataclasses import dataclass
from uuid import UUID

from app.application.exceptions import SectionNotFoundError
from app.application.interfaces.repositories.section_repository import SectionRepository
from app.domain.entities.section import Section


@dataclass(slots=True)
class UpdateSectionCommand:
    section_id: UUID
    title: str
    description: str
    position: int


class UpdateSectionUseCase:
    def __init__(self, section_repository: SectionRepository) -> None:
        self.section_repository = section_repository

    async def execute(self, command: UpdateSectionCommand) -> Section:
        section = await self.section_repository.get_by_id(command.section_id)
        if section is None:
            raise SectionNotFoundError("Section not found.")

        section.update(
            title=command.title,
            description=command.description,
            position=command.position,
        )
        await self.section_repository.update(section)
        return section
