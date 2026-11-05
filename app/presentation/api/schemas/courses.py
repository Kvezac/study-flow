from pydantic import BaseModel, Field


class CourseWriteRequest(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1)


class CreateCourseRequest(CourseWriteRequest):
    pass


class UpdateCourseRequest(CourseWriteRequest):
    pass
