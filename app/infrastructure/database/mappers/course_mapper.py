from uuid import UUID

from app.domain.entities.course import Course
from app.infrastructure.database.models.course_model import CourseModel


class CourseMapper:
    @staticmethod
    def to_domain(model: CourseModel) -> Course:
        return Course(
            id=UUID(model.id),
            title=model.title,
            description=model.description,
            module_ids=[
                UUID(module.id)
                for module in sorted(model.modules, key=lambda x: x.position)
            ],
        )

    @staticmethod
    def to_model(entity: Course) -> CourseModel:
        return CourseModel(
            id=str(entity.id),
            title=entity.title,
            description=entity.description,
        )
