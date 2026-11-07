from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.interfaces.repositories.user_repository import UserRepository
from app.domain.entities.user import User
from app.infrastructure.database.mappers.user_mapper import UserMapper
from app.infrastructure.database.models.user_model import UserModel


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, user_id: UUID) -> User | None:
        model = await self.session.get(UserModel, str(user_id))
        return None if model is None else UserMapper.to_domain(model)

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return None if model is None else UserMapper.to_domain(model)

    async def add(self, user: User) -> None:
        self.session.add(UserMapper.to_model(user))
        await self.session.flush()
