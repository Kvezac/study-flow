from dataclasses import dataclass

from app.application.dto.auth_token import AuthToken
from app.application.exceptions import InvalidCredentialsError
from app.application.interfaces.services.password_hasher import PasswordHasher
from app.application.interfaces.services.token_service import TokenService
from app.application.interfaces.unit_of_work import UnitOfWork


@dataclass(slots=True)
class LoginUserCommand:
    email: str
    password: str


class LoginUserUseCase:
    def __init__(
        self,
        uow: UnitOfWork,
        password_hasher: PasswordHasher,
        token_service: TokenService,
    ) -> None:
        self.uow = uow
        self.password_hasher = password_hasher
        self.token_service = token_service

    async def execute(self, command: LoginUserCommand) -> AuthToken:
        async with self.uow:
            user = await self.uow.users.get_by_email(command.email)
            if user is None:
                raise InvalidCredentialsError("Invalid email or password.")

            is_valid_password = self.password_hasher.verify(
                command.password,
                user.hashed_password,
            )
            if not is_valid_password:
                raise InvalidCredentialsError("Invalid email or password.")

            access_token = self.token_service.create_access_token(
                user_id=user.id,
                role=user.role.value,
            )
            return AuthToken(access_token=access_token)
