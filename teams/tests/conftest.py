import pytest
from typing import AsyncGenerator
from datetime import date
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from src.db.models import Base, Team
from src.api.dependencies import get_db_session


@pytest.fixture(scope="session")
async def test_engine():
    """Create a test database engine."""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=True,
    )
    yield engine
    await engine.dispose()


@pytest.fixture(scope="session")
def test_sessionmaker(test_engine):
    """Create a test sessionmaker."""
    return async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


@pytest.fixture(scope="function")
async def test_db(test_engine, test_sessionmaker) -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session that rolls back changes after each test."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # connect to the database
    connection = await test_engine.connect()
    # begin a transaction
    trans = await connection.begin()

    # bind an individual session to the connection
    session = test_sessionmaker()

    try:
        yield session
    finally:
        await session.close()
        # rollback the transaction
        await trans.rollback()
        # return connection to the Engine
        await connection.close()

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def async_client(test_db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """
    Provide a test client that overrides the repository dependencies
    to use instances created with the isolated test database.
    """
    
    async def override_get_db_session() -> AsyncGenerator[AsyncSession, None]:
        yield test_db

    # Apply the overrides for the repository dependencies
    app.dependency_overrides[get_db_session] = override_get_db_session

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

    # Clean up the overrides after the test
    app.dependency_overrides.clear()


@pytest.fixture
def sample_team_data():
    """Sample team data for testing."""
    return {
        "name": "Test Team",
        "country": "USA",
        "city": "New York",
        "founded_year": 2020,
        "logo_url": "https://example.com/logo.png"
    }


@pytest.fixture
async def sample_team_in_db(test_db, sample_team_data):
    """Create a sample team in the database."""
    team = Team(**sample_team_data)
    test_db.add(team)
    await test_db.commit()
    await test_db.refresh(team)
    return team
