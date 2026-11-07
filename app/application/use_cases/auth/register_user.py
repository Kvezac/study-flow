from dataclasses import dataclass
from uuid import uuid4

from app.application.exceptions import UserAlreadyExistsError
from app.application.interfaces.services.password_hasher import PasswordHasher
from app.application.interfaces.unit_of_work import UnitOfWork
from app.domain.entities.user import User, UserRole


@dataclass(slots=True)
class RegisterUserCommand:
    email: str
    password: str


class RegisterUserUseCase:
    def __init__(self, uow: UnitOfWork, password_hasher: PasswordHasher) -> None:
        self.uow = uow
        self.password_hasher = password_hasher

    async def execute(self, command: RegisterUserCommand) -> User:
        async with self.uow:
            existing_user = await self.uow.users.get_by_email(command.email)
            if existing_user is not None:
                raise UserAlreadyExistsError('User with this email already exists.')

            user = User(
                id=uuid4(),
                email=command.email,
                hashed_password=self.password_hasher.hash(command.password),
                role=UserRole.STUDENT,
            )

            await self.uow.users.add(user)
            await self.uow.commit()
            return user