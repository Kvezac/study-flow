from dataclasses import dataclass
from uuid import UUID

from app.application.exceptions import ModuleNotFoundError
from app.application.interfaces.repositories.module_repository import ModuleRepository
from app.domain.entities.module import Module


@dataclass(slots=True)
class UpdateModuleCommand:
    module_id: UUID
    title: str
    description: str
    position: int


class UpdateModuleUseCase:
    def __init__(self, module_repository: ModuleRepository) -> None:
        self.module_repository = module_repository

    async def execute(self, command: UpdateModuleCommand) -> Module:
        module = await self.module_repository.get_by_id(command.module_id)
        if module is None:
            raise ModuleNotFoundError("Module not found.")

        module.update(
            title=command.title,
            description=command.description,
            position=command.position,
        )
        await self.module_repository.update(module)
        return module
