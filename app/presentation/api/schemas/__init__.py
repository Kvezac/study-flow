from app.presentation.api.schemas.auth import (
    CurrentUserResponse,
    LoginRequest,
    RegisteredUserResponse,
    RegisterUserRequest,
    TokenResponse,
)
from app.presentation.api.schemas.content import (
    CourseListItemResponse,
    CourseResponse,
    CourseStructureResponse,
    LectureResponse,
    LectureStructureResponse,
    ModuleStructureResponse,
    SectionStructureResponse,
)
from app.presentation.api.schemas.courses import (
    CreateCourseRequest,
    UpdateCourseRequest,
)
from app.presentation.api.schemas.errors import ErrorResponse
from app.presentation.api.schemas.lectures import (
    CreateLectureRequest,
    UpdateLectureRequest,
)
from app.presentation.api.schemas.modules import (
    CreateModuleRequest,
    ModuleResponse,
    UpdateModuleRequest,
)
from app.presentation.api.schemas.sections import (
    CreateSectionRequest,
    SectionResponse,
    UpdateSectionRequest,
)

__all__ = [
    "CourseListItemResponse",
    "CourseResponse",
    "CourseStructureResponse",
    "CreateCourseRequest",
    "CreateLectureRequest",
    "CreateModuleRequest",
    "CreateSectionRequest",
    "CurrentUserResponse",
    "ErrorResponse",
    "LectureResponse",
    "LectureStructureResponse",
    "LoginRequest",
    "ModuleResponse",
    "ModuleStructureResponse",
    "RegisterUserRequest",
    "RegisteredUserResponse",
    "SectionResponse",
    "SectionStructureResponse",
    "TokenResponse",
    "UpdateCourseRequest",
    "UpdateLectureRequest",
    "UpdateModuleRequest",
    "UpdateSectionRequest",
]
