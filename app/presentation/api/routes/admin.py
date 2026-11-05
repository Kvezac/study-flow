from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.application.use_cases.courses.create_course import (
    CreateCourseCommand,
    CreateCourseUseCase,
)
from app.application.use_cases.courses.update_course import (
    UpdateCourseCommand,
    UpdateCourseUseCase,
)
from app.application.use_cases.lectures.create_lecture import (
    CreateLectureCommand,
    CreateLectureUseCase,
)
from app.application.use_cases.lectures.update_lecture import (
    UpdateLectureCommand,
    UpdateLectureUseCase,
)
from app.application.use_cases.modules.create_module import (
    CreateModuleCommand,
    CreateModuleUseCase,
)
from app.application.use_cases.modules.update_module import (
    UpdateModuleCommand,
    UpdateModuleUseCase,
)
from app.application.use_cases.sections.create_section import (
    CreateSectionCommand,
    CreateSectionUseCase,
)
from app.application.use_cases.sections.update_section import (
    UpdateSectionCommand,
    UpdateSectionUseCase,
)
from app.presentation.api.dependencies import (
    get_create_course_use_case,
    get_create_lecture_use_case,
    get_create_module_use_case,
    get_create_section_use_case,
    get_update_course_use_case,
    get_update_lecture_use_case,
    get_update_module_use_case,
    get_update_section_use_case,
)
from app.presentation.api.schemas import (
    CourseResponse,
    CreateCourseRequest,
    CreateLectureRequest,
    CreateModuleRequest,
    CreateSectionRequest,
    LectureResponse,
    ModuleResponse,
    SectionResponse,
    UpdateCourseRequest,
    UpdateLectureRequest,
    UpdateModuleRequest,
    UpdateSectionRequest,
    ErrorResponse,
)

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post(
    "/courses",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_course(
    request: CreateCourseRequest,
    use_case: CreateCourseUseCase = Depends(get_create_course_use_case),
) -> CourseResponse:
    result = await use_case.execute(
        CreateCourseCommand(title=request.title, description=request.description)
    )
    return CourseResponse.model_validate(result)


@router.put(
    "/courses/{course_id}",
    response_model=CourseResponse,
)
async def update_course(
    course_id: UUID,
    request: UpdateCourseRequest,
    use_case: UpdateCourseUseCase = Depends(get_update_course_use_case),
) -> CourseResponse:
    result = await use_case.execute(
        UpdateCourseCommand(
            course_id=course_id,
            title=request.title,
            description=request.description,
        )
    )
    return CourseResponse.model_validate(result)


@router.post(
    "/courses/{course_id}/modules",
    response_model=ModuleResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_module(
    course_id: UUID,
    request: CreateModuleRequest,
    use_case: CreateModuleUseCase = Depends(get_create_module_use_case),
) -> ModuleResponse:
    result = await use_case.execute(
        CreateModuleCommand(
            course_id=course_id,
            title=request.title,
            description=request.description,
            position=request.position,
        )
    )
    return ModuleResponse.model_validate(result)


@router.put(
    "/modules/{module_id}",
    response_model=ModuleResponse,
)
async def update_module(
    module_id: UUID,
    request: UpdateModuleRequest,
    use_case: UpdateModuleUseCase = Depends(get_update_module_use_case),
) -> ModuleResponse:
    result = await use_case.execute(
        UpdateModuleCommand(
            module_id=module_id,
            title=request.title,
            description=request.description,
            position=request.position,
        )
    )
    return ModuleResponse.model_validate(result)


@router.post(
    "/modules/{module_id}/sections",
    response_model=SectionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_section(
    module_id: UUID,
    request: CreateSectionRequest,
    use_case: CreateSectionUseCase = Depends(get_create_section_use_case),
) -> SectionResponse:
    result = await use_case.execute(
        CreateSectionCommand(
            module_id=module_id,
            title=request.title,
            description=request.description,
            position=request.position,
        )
    )
    return SectionResponse.model_validate(result)


@router.put(
    "/sections/{section_id}",
    response_model=SectionResponse,
)
async def update_section(
    section_id: UUID,
    request: UpdateSectionRequest,
    use_case: UpdateSectionUseCase = Depends(get_update_section_use_case),
) -> SectionResponse:
    result = await use_case.execute(
        UpdateSectionCommand(
            section_id=section_id,
            title=request.title,
            description=request.description,
            position=request.position,
        )
    )
    return SectionResponse.model_validate(result)

@router.post(
    "/sections/{section_id}/lectures",
    response_model=LectureResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_lecture(
    section_id: UUID,
    request: CreateLectureRequest,
    use_case: CreateLectureUseCase = Depends(get_create_lecture_use_case),
) -> LectureResponse:
    result = await use_case.execute(
        CreateLectureCommand(
            section_id=section_id,
            title=request.title,
            content=request.content,
            position=request.position,
        )
    )
    return LectureResponse.model_validate(result)


@router.put(
    "/lectures/{lecture_id}",
    response_model=LectureResponse,
)
async def update_lecture(
    lecture_id: UUID,
    request: UpdateLectureRequest,
    use_case: UpdateLectureUseCase = Depends(get_update_lecture_use_case),
) -> LectureResponse:
    result = await use_case.execute(
        UpdateLectureCommand(
            lecture_id=lecture_id,
            title=request.title,
            content=request.content,
            position=request.position,
        )
    )
    return LectureResponse.model_validate(result)