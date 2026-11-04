from dataclasses import dataclass, field
from uuid import UUID


@dataclass(slots=True)
class LectureStructureDTO:
    id: UUID
    title: str
    position: int


@dataclass(slots=True)
class SectionStructureDTO:
    id: UUID
    title: str
    description: str
    position: int
    lectures: list[LectureStructureDTO] = field(default_factory=list)


@dataclass(slots=True)
class ModuleStructureDTO:
    id: UUID
    title: str
    description: str
    position: int
    sections: list[SectionStructureDTO] = field(default_factory=list)


@dataclass(slots=True)
class CourseStructureDTO:
    id: UUID
    title: str
    description: str
    modules: list[ModuleStructureDTO] = field(default_factory=list)
