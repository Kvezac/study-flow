from uuid import UUID

from app.domain.entities.lecture import Lecture
from app.infrastructure.database.models.lecture_model import LectureModel


class LectureMapper:
    @staticmethod
    def to_domain(model: LectureModel) -> Lecture:
        return Lecture(
            id=UUID(model.id),
            section_id=UUID(model.section_id),
            title=model.title,
            content=model.content,
            position=model.position,
        )

    @staticmethod
    def to_model(entity: Lecture) -> LectureModel:
        return LectureModel(
            id=str(entity.id),
            section_id=str(entity.section_id),
            title=entity.title,
            content=entity.content,
            position=entity.position,
        )
