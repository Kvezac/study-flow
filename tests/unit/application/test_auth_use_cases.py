from uuid import uuid4
import pytest

from app.application.exceptions import UserAlreadyExistsError
from app.application.use_cases.auth.register_user import (
    RegisterUserCommand,
    RegisterUserUseCase,
)
from app.application.exceptions import InvalidCredentialsError
from app.application.use_cases.auth.login_user import LoginUserCommand, LoginUserUseCase
from app.domain.entities.user import User, UserRole
from app.application.interfaces.unit_of_work import UnitOfWork
from app.application.interfaces.repositories import (
    UserRepository,
)


class FakeUserRepository(UserRepository):
    def __init__(self) -> None:
        self.items: dict[str, User] = {}

    async def get_by_id(self, user_id):
        for user in self.items.values():
            if user.id == user_id:
                return user
        return None

    async def get_by_email(self, email: str):
        return self.items.get(email)

    async def add(self, user: User) -> None:
        self.items[user.email] = user


class FakeUnitOfWork(UnitOfWork):
    def __init__(self) -> None:
        self.users = FakeUserRepository()
        self.committed = False

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return None

    async def commit(self) -> None:
        self.committed = True

    async def rollback(self) -> None:
        return None


class StubPasswordHasher:
    def hash(self, raw_password: str) -> str:
        return f'hashed::{raw_password}'

    def verify(self, raw_password: str, hashed_password: str) -> bool:
        return hashed_password == f'hashed::{raw_password}'


class StubTokenService:
    def create_access_token(self, user_id, role: str) -> str:
        return f'token-for-{user_id}-{role}'

    def get_user_id(self, token: str):
        raise NotImplementedError

@pytest.mark.asyncio
async def test_register_user_creates_student_and_commits() -> None:
    uow = FakeUnitOfWork()
    use_case = RegisterUserUseCase(uow=uow, password_hasher=StubPasswordHasher())

    result = await use_case.execute(
        RegisterUserCommand(
            email='student@example.com',
            password='secret123',
        )
    )

    assert result.email == 'student@example.com'
    assert result.role is UserRole.STUDENT
    assert result.hashed_password == 'hashed::secret123'
    assert uow.committed is True


@pytest.mark.asyncio
async def test_register_user_raises_error_when_email_already_exists() -> None:
    uow = FakeUnitOfWork()
    existing_user = User(
        id=uuid4(),
        email='student@example.com',
        hashed_password='hashed::secret123',
        role=UserRole.STUDENT,
    )
    await uow.users.add(existing_user)

    use_case = RegisterUserUseCase(uow=uow, password_hasher=StubPasswordHasher())

    with pytest.raises(UserAlreadyExistsError):
        await use_case.execute(
            RegisterUserCommand(
                email='student@example.com',
                password='another-password',
            )
        )

@pytest.mark.asyncio
async def test_login_user_returns_access_token() -> None:
    uow = FakeUnitOfWork()
    user = User(
        id=uuid4(),
        email='admin@example.com',
        hashed_password='hashed::secret123',
        role=UserRole.ADMIN,
    )
    await uow.users.add(user)

    use_case = LoginUserUseCase(
        uow=uow,
        password_hasher=StubPasswordHasher(),
        token_service=StubTokenService(),
    )

    result = await use_case.execute(
        LoginUserCommand(
            email='admin@example.com',
            password='secret123',
        )
    )

    assert result.token_type == 'bearer'
    assert result.access_token.startswith('token-for-')


@pytest.mark.asyncio
async def test_login_user_raises_error_when_email_is_unknown() -> None:
    use_case = LoginUserUseCase(
        uow=FakeUnitOfWork(),
        password_hasher=StubPasswordHasher(),
        token_service=StubTokenService(),
    )

    with pytest.raises(InvalidCredentialsError):
        await use_case.execute(
            LoginUserCommand(
                email='missing@example.com',
                password='secret123',
            )
        )


@pytest.mark.asyncio
async def test_login_user_raises_error_when_password_is_invalid() -> None:
    uow = FakeUnitOfWork()
    user = User(
        id=uuid4(),
        email='admin@example.com',
        hashed_password='hashed::secret123',
        role=UserRole.ADMIN,
    )
    await uow.users.add(user)

    use_case = LoginUserUseCase(
        uow=uow,
        password_hasher=StubPasswordHasher(),
        token_service=StubTokenService(),
    )

    with pytest.raises(InvalidCredentialsError):
        await use_case.execute(
            LoginUserCommand(
                email='admin@example.com',
                password='wrong-password',
            )
        )