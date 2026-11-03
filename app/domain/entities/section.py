from dataclasses import dataclass, field
from uuid import UUID

from app.domain.exceptions import InvalidSectionError


@dataclass(slots=True)
class Section:
    id: UUID
    module_id: UUID
    title: str
    description: str = ""
    position: int = 1
    lecture_ids: list[UUID] = field(default_factory=list)

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        if not self.title or not self.title.strip():
            raise InvalidSectionError("Section title cannot be empty.")
        if self.position < 1:
            raise InvalidSectionError("Section position must be positive.")

    def update(self, title: str, description: str, position: int) -> None:
        self.title = title
        self.description = description
        self.position = position
        self._validate()

    def add_lecture(self, lecture_id: UUID) -> None:
        if lecture_id not in self.lecture_ids:
            self.lecture_ids.append(lecture_id)
