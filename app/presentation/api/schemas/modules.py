from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ModuleWriteRequest(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1)
    position: int = Field(ge=1)


class CreateModuleRequest(ModuleWriteRequest):
    pass


class UpdateModuleRequest(ModuleWriteRequest):
    pass


class ModuleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    course_id: UUID
    title: str
    description: str
    position: int
