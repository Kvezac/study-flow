from uuid import UUID

from app.domain.entities.module import Module
from app.infrastructure.database.models.module_model import ModuleModel


class ModuleMapper:
    @staticmethod
    def to_domain(model: ModuleModel) -> Module:
        return Module(
            id=UUID(model.id),
            course_id=UUID(model.course_id),
            title=model.title,
            description=model.description,
            position=model.position,
            section_ids=[
                UUID(section.id)
                for section in sorted(model.sections, key=lambda x: x.position)
            ],
        )

    @staticmethod
    def to_model(entity: Module) -> ModuleModel:
        return ModuleModel(
            id=str(entity.id),
            course_id=str(entity.course_id),
            title=entity.title,
            description=entity.description,
            position=entity.position,
        )
