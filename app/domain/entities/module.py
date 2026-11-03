from dataclasses import dataclass, field
from uuid import UUID

from app.domain.exceptions import InvalidModuleError


@dataclass(slots=True)
class Module:
    id: UUID
    course_id: UUID
    title: str
    description: str
    position: int
    section_ids: list[UUID] = field(default_factory=list)

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        if not self.title or not self.title.strip():
            raise InvalidModuleError("Module title cannot be empty.")
        if not self.description or not self.description.strip():
            raise InvalidModuleError("Module description cannot be empty.")
        if self.position < 1:
            raise InvalidModuleError("Module position must be positive.")

    def update(self, title: str, description: str, position: int) -> None:
        self.title = title
        self.description = description
        self.position = position
        self._validate()

    def add_section(self, section_id: UUID) -> None:
        if section_id not in self.section_ids:
            self.section_ids.append(section_id)
