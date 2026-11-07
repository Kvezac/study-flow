from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.application.use_cases.auth.login_user import LoginUserCommand, LoginUserUseCase
from app.application.use_cases.auth.register_user import (
    RegisterUserCommand,
    RegisterUserUseCase,
)
from app.domain.entities.user import User
from app.presentation.api.dependencies import (
    get_current_user,
    get_login_user_use_case,
    get_register_user_use_case,
)
from app.presentation.api.schemas import (
    CurrentUserResponse,
    ErrorResponse,
    LoginRequest,
    RegisteredUserResponse,
    RegisterUserRequest,
    TokenResponse,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=RegisteredUserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
    description=(
        "Creates a new user account in the system. "
        "A public registration always creates a user with the student role."
    ),
    responses={
        400: {
            "description": "Domain or application validation error.",
            "model": ErrorResponse,
        },
    },
)
async def register_user(
    request: RegisterUserRequest,
    use_case: Annotated[RegisterUserUseCase, Depends(get_register_user_use_case)],
) -> RegisteredUserResponse:
    result = await use_case.execute(
        RegisterUserCommand(
            email=request.email,
            password=request.password,
        )
    )
    return RegisteredUserResponse.model_validate(result)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login user",
    description=(
        "Authenticates a user by email and password and returns a JWT access token."
    ),
    responses={
        400: {
            "description": "Invalid email or password.",
            "model": ErrorResponse,
        },
    },
)
async def login_user(
    request: LoginRequest,
    use_case: Annotated[LoginUserUseCase, Depends(get_login_user_use_case)],
) -> TokenResponse:
    result = await use_case.execute(
        LoginUserCommand(
            email=request.email,
            password=request.password,
        )
    )
    return TokenResponse(
        access_token=result.access_token,
        token_type=result.token_type,
    )


@router.get(
    "/me",
    response_model=CurrentUserResponse,
    summary="Get current user",
    description="Returns the currently authenticated user resolved from Bearer token.",
    responses={
        401: {
            "description": "Authentication credentials are missing or invalid.",
            "model": ErrorResponse,
        },
    },
)
async def get_me(
    current_user: Annotated[User, Depends(get_current_user)],
) -> CurrentUserResponse:
    return CurrentUserResponse.model_validate(current_user)
