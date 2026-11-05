from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class SectionWriteRequest(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str = ""
    position: int = Field(ge=1)


class CreateSectionRequest(SectionWriteRequest):
    pass


class UpdateSectionRequest(SectionWriteRequest):
    pass


class SectionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    module_id: UUID
    title: str
    description: str
    position: int
