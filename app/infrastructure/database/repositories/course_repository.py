from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.application.interfaces.repositories.course_repository import CourseRepository
from app.domain.entities.course import Course
from app.infrastructure.database.mappers.course_mapper import CourseMapper
from app.infrastructure.database.models.course_model import CourseModel


class SqlAlchemyCourseRepository(CourseRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, course_id: UUID) -> Course | None:
        stmt = (
            select(CourseModel)
            .options(selectinload(CourseModel.modules))
            .where(CourseModel.id == str(course_id))
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return None if model is None else CourseMapper.to_domain(model)

    async def list(self) -> list[Course]:
        stmt = select(CourseModel).options(selectinload(CourseModel.modules))
        result = await self.session.execute(stmt)
        return [CourseMapper.to_domain(model) for model in result.scalars().all()]

    async def add(self, course: Course) -> None:
        self.session.add(CourseMapper.to_model(course))
        await self.session.flush()

    async def update(self, course: Course) -> None:
        model = await self.session.get(CourseModel, str(course.id))
        if model is None:
            return
        model.title = course.title
        model.description = course.description
        await self.session.flush()

    async def remove(self, course_id: UUID) -> None:
        model = await self.session.get(CourseModel, str(course_id))
        if model is None:
            return
        await self.session.delete(model)
        await self.session.flush()
