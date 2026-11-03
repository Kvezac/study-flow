from dataclasses import dataclass, field
from uuid import UUID

from app.domain.exceptions import InvalidCourseError


@dataclass(slots=True)
class Course:
    id: UUID
    title: str
    description: str
    module_ids: list[UUID] = field(default_factory=list)

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        if not self.title or not self.title.strip():
            raise InvalidCourseError("Course title cannot be empty.")
        if not self.description or not self.description.strip():
            raise InvalidCourseError("Course description cannot be empty.")

    def update(self, title: str, description: str) -> None:
        self.title = title
        self.description = description
        self._validate()

    def add_module(self, module_id: UUID) -> None:
        if module_id not in self.module_ids:
            self.module_ids.append(module_id)
