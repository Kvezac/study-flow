from uuid import UUID

from app.domain.entities.section import Section
from app.infrastructure.database.models.section_model import SectionModel


class SectionMapper:
    @staticmethod
    def to_domain(model: SectionModel) -> Section:
        return Section(
            id=UUID(model.id),
            module_id=UUID(model.module_id),
            title=model.title,
            description=model.description,
            position=model.position,
            lecture_ids=[
                UUID(lecture.id)
                for lecture in sorted(model.lectures, key=lambda x: x.position)
            ],
        )

    @staticmethod
    def to_model(entity: Section) -> SectionModel:
        return SectionModel(
            id=str(entity.id),
            module_id=str(entity.module_id),
            title=entity.title,
            description=entity.description,
            position=entity.position,
        )