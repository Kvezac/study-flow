from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.application.interfaces.repositories.section_repository import SectionRepository
from app.domain.entities.section import Section
from app.infrastructure.database.mappers.section_mapper import SectionMapper
from app.infrastructure.database.models.section_model import SectionModel


class SqlAlchemySectionRepository(SectionRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, section_id: UUID) -> Section | None:
        stmt = (
            select(SectionModel)
            .options(selectinload(SectionModel.lectures))
            .where(SectionModel.id == str(section_id))
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return None if model is None else SectionMapper.to_domain(model)

    async def get_by_ids(self, section_ids: list[UUID]) -> list[Section]:
        if not section_ids:
            return []
        stmt = (
            select(SectionModel)
            .options(selectinload(SectionModel.lectures))
            .where(SectionModel.id.in_([str(item) for item in section_ids]))
        )
        result = await self.session.execute(stmt)
        return [SectionMapper.to_domain(model) for model in result.scalars().all()]

    async def add(self, section: Section) -> None:
        self.session.add(SectionMapper.to_model(section))
        await self.session.flush()

    async def update(self, section: Section) -> None:
        model = await self.session.get(SectionModel, str(section.id))
        if model is None:
            return
        model.title = section.title
        model.description = section.description
        model.position = section.position
        await self.session.flush()
