from dataclasses import dataclass
from uuid import UUID

from app.application.dto.course_structure import (
    CourseStructureDTO,
    LectureStructureDTO,
    ModuleStructureDTO,
    SectionStructureDTO,
)
from app.application.exceptions import CourseNotFoundError
from app.application.interfaces.repositories.course_repository import CourseRepository
from app.application.interfaces.repositories.lecture_repository import LectureRepository
from app.application.interfaces.repositories.module_repository import ModuleRepository
from app.application.interfaces.repositories.section_repository import SectionRepository


@dataclass(slots=True)
class GetCourseStructureQuery:
    course_id: UUID


class GetCourseStructureUseCase:
    def __init__(
        self,
        course_repository: CourseRepository,
        module_repository: ModuleRepository,
        section_repository: SectionRepository,
        lecture_repository: LectureRepository,
    ) -> None:
        self.course_repository = course_repository
        self.module_repository = module_repository
        self.section_repository = section_repository
        self.lecture_repository = lecture_repository

    async def execute(self, query: GetCourseStructureQuery) -> CourseStructureDTO:
        course = await self.course_repository.get_by_id(query.course_id)
        if course is None:
            raise CourseNotFoundError("Course not found.")

        return CourseStructureDTO(
            id=course.id,
            title=course.title,
            description=course.description,
            modules=await self._build_modules(course.module_ids),
        )

    async def _build_modules(self, module_ids: list[UUID]) -> list[ModuleStructureDTO]:
        modules = await self.module_repository.get_by_ids(module_ids)
        return [
            ModuleStructureDTO(
                id=module.id,
                title=module.title,
                description=module.description,
                position=module.position,
                sections=await self._build_sections(module.section_ids),
            )
            for module in sorted(modules, key=lambda item: item.position)
        ]

    async def _build_sections(
        self, section_ids: list[UUID]
    ) -> list[SectionStructureDTO]:
        sections = await self.section_repository.get_by_ids(section_ids)
        return [
            SectionStructureDTO(
                id=section.id,
                title=section.title,
                description=section.description,
                position=section.position,
                lectures=await self._build_lectures(section.lecture_ids),
            )
            for section in sorted(sections, key=lambda item: item.position)
        ]

    async def _build_lectures(
        self, lecture_ids: list[UUID]
    ) -> list[LectureStructureDTO]:
        lectures = await self.lecture_repository.get_by_ids(lecture_ids)
        return [
            LectureStructureDTO(
                id=lecture.id,
                title=lecture.title,
                position=lecture.position,
            )
            for lecture in sorted(lectures, key=lambda item: item.position)
        ]
