from dataclasses import dataclass
from uuid import UUID

from app.application.exceptions import ModuleNotFoundError
from app.application.interfaces.unit_of_work import UnitOfWork
from app.domain.entities.module import Module


@dataclass(slots=True)
class UpdateModuleCommand:
    module_id: UUID
    title: str
    description: str
    position: int


class UpdateModuleUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def execute(self, command: UpdateModuleCommand) -> Module:
        async with self.uow:
            module = await self.uow.modules.get_by_id(command.module_id)
            if module is None:
                raise ModuleNotFoundError("Module not found.")

            module.update(
                title=command.title,
                description=command.description,
                position=command.position,
            )
            await self.uow.modules.update(module)
            await self.uow.commit()
            return module
