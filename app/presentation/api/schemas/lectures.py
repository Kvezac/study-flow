from pydantic import BaseModel, Field


class LectureWriteRequest(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    content: str = Field(min_length=1)
    position: int = Field(ge=1)


class CreateLectureRequest(LectureWriteRequest):
    pass


class UpdateLectureRequest(LectureWriteRequest):
    pass
