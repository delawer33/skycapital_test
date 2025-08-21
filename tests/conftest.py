import pytest_asyncio
import asyncio
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from app.db.base import Base, get_async_db_session
from app.models import *
from app.main import app
from httpx import AsyncClient, ASGITransport

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine_test = create_async_engine(TEST_DATABASE_URL, future=True, echo=False)
SessionTest = async_sessionmaker(
    engine_test, expire_on_commit=False, class_=AsyncSession
)


@pytest_asyncio.fixture(scope="session", autouse=True)
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    print("!!" * 200)
    async with engine_test.begin() as conn:
        print(Base.metadata, "!!!!!!!!!!!!!!!!!!!!!")
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="module")
async def db_session():
    async with SessionTest() as session:
        yield session


@pytest_asyncio.fixture(scope="module")
async def client(db_session):
    async def override_get_async_db_session():
        async with SessionTest() as session:
            yield session

    app.dependency_overrides[get_async_db_session] = (
        override_get_async_db_session
    )
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver/api/v1"
    ) as ac:
        yield ac
    app.dependency_overrides.clear()
