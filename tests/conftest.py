import os
from collections.abc import AsyncIterator
from types import SimpleNamespace
from uuid import uuid4
from pathlib import Path

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

import app.presentation.api.dependencies as api_dependencies
from app.infrastructure.database.models import (
    Base,
    CourseModel,
    LectureModel,
    ModuleModel,
    SectionModel,
    UserModel,
)
from app.infrastructure.security.password_hasher import PwdlibPasswordHasher
from app.main import create_app

@pytest_asyncio.fixture(scope='session')
async def test_engine(tmp_path_factory) -> AsyncIterator:
    database_dir = tmp_path_factory.mktemp("test_db")
    database_path = Path(database_dir) / "test_fastapi_education.db"
    database_url = f"sqlite+aiosqlite:///{database_path}"

    engine = create_async_engine(database_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()
    if database_path.exists():
        os.remove(database_path)

@pytest.fixture
def session_factory(test_engine):
    return async_sessionmaker(bind=test_engine, expire_on_commit=False)

@pytest_asyncio.fixture
async def app(session_factory):
    app = create_app()
    original_session_factory = api_dependencies.SessionFactory
    api_dependencies.SessionFactory = session_factory
    try:
        yield app
    finally:
        api_dependencies.SessionFactory = original_session_factory

@pytest_asyncio.fixture
async def client(app) -> AsyncIterator[AsyncClient]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://test') as client:
        yield client

@pytest_asyncio.fixture(autouse=True)
async def clear_database(session_factory) -> None:
    async with session_factory() as session:
        for model in [LectureModel, SectionModel, ModuleModel, CourseModel, UserModel]:
            await session.execute(delete(model))
        await session.commit()

@pytest_asyncio.fixture
async def seeded_course_tree(session_factory):
    course_id = str(uuid4())
    module_id = str(uuid4())
    section_id = str(uuid4())
    lecture_id = str(uuid4())

    async with session_factory() as session:
        course = CourseModel(
            id=course_id,
            title='FastAPI course',
            description='Clean architecture in practice.',
        )
        module = ModuleModel(
            id=module_id,
            course_id=course_id,
            title='MVP stage',
            description='Content, users and access.',
            position=1,
        )
        section = SectionModel(
            id=section_id,
            module_id=module_id,
            title='Auth section',
            description='JWT and route protection.',
            position=1,
        )
        lecture = LectureModel(
            id=lecture_id,
            section_id=section_id,
            title='Bearer token in practice',
            content='Lecture content',
            position=1,
        )
        session.add_all([course, module, section, lecture])
        await session.commit()

    return SimpleNamespace(
        course_id=course_id,
        module_id=module_id,
        section_id=section_id,
        lecture_id=lecture_id,
        course_title='FastAPI course',
        lecture_content='Lecture content',
    )

@pytest_asyncio.fixture
async def seeded_student_user(session_factory):
    hasher = PwdlibPasswordHasher()
    async with session_factory() as session:
        user = UserModel(
            id=str(uuid4()),
            email='student@example.com',
            hashed_password=hasher.hash('strongpassword123'),
            role='student',
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

@pytest_asyncio.fixture
async def seeded_admin_user(session_factory):
    hasher = PwdlibPasswordHasher()
    async with session_factory() as session:
        user = UserModel(
            id=str(uuid4()),
            email='admin@example.com',
            hashed_password=hasher.hash('strongpassword123'),
            role='admin',
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

@pytest_asyncio.fixture
async def student_auth_headers(client, seeded_student_user):
    response = await client.post(
        '/api/auth/login',
        json={
            'email': 'student@example.com',
            'password': 'strongpassword123',
        },
    )
    token = response.json()['access_token']
    return {'Authorization': f'Bearer {token}'}


@pytest_asyncio.fixture
async def admin_auth_headers(client, seeded_admin_user):
    response = await client.post(
        '/api/auth/login',
        json={
            'email': 'admin@example.com',
            'password': 'strongpassword123',
        },
    )
    token = response.json()['access_token']
    return {'Authorization': f'Bearer {token}'}