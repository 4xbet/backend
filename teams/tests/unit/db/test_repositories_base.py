import pytest
from unittest.mock import Mock, AsyncMock, patch
from src.db.repositories.base import BaseRepository
from src.db.models import Team, Athlete


class TestBaseRepository:
    """Unit tests for BaseRepository."""

    @pytest.fixture
    def mock_database(self, mock_session):
        """Create mock database."""
        database = Mock()
        database.get_session.return_value = mock_session
        return database

    @pytest.fixture
    def mock_session(self):
        """Create mock database session."""
        session = AsyncMock()
        
        # Set up the proper mock chain for execute().scalars().first()/all()
        mock_result = Mock()  # result is not async
        mock_scalars = Mock()  # scalars is not async
        
        # Configure the chain: session.execute() -> result -> scalars -> scalars_result
        session.execute = AsyncMock(return_value=mock_result)
        mock_result.scalars = Mock(return_value=mock_scalars)
        mock_scalars.first = Mock(return_value=None)  # first() is sync, not async
        mock_scalars.all = Mock(return_value=[])  # all() is sync, not async
        
        # Other session methods
        session.get = AsyncMock()
        session.add = Mock()
        session.delete = AsyncMock()  # delete should be async
        session.commit = AsyncMock()
        session.refresh = AsyncMock()
        session.close = AsyncMock()
        
        # This is the crucial part to make it a proper async context manager
        async def __aenter__(*args):
            return session
        
        async def __aexit__(*args):
            pass

        session.__aenter__ = __aenter__
        session.__aexit__ = __aexit__
        return session

    @pytest.fixture
    def test_repository(self, mock_database):
        """Create test repository implementation."""
        class TestRepository(BaseRepository[Team]):
            def get_model(self):
                return Team
        return TestRepository(mock_database)

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_get_existing_entity(self, test_repository, mock_database, mock_session):
        """Test getting existing entity."""
        # Arrange
        expected_team = Team(id=1, name="Test Team", country="USA", founded_year=2020)
        # Set up the mock chain to return the expected team
        mock_session.execute.return_value.scalars.return_value.first.return_value = expected_team
        
        # Act
        result = await test_repository.get(1)
        
        # Assert
        assert result == expected_team
        mock_session.execute.assert_called_once()
        mock_session.commit.assert_not_called()

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_get_non_existing_entity(self, test_repository, mock_database, mock_session):
        """Test getting non-existing entity."""
        # Arrange
        mock_session.execute.return_value.scalars.return_value.first.return_value = None
        
        # Act
        result = await test_repository.get(999)
        
        # Assert
        assert result is None
        mock_session.execute.assert_called_once()

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_list_with_limit_offset(self, test_repository, mock_database, mock_session):
        """Test listing entities with limit and offset."""
        # Arrange
        teams = [
            Team(id=1, name="Team 1", country="USA", founded_year=2020),
            Team(id=2, name="Team 2", country="Canada", founded_year=2021)
        ]
        mock_session.execute.return_value.scalars.return_value.all.return_value = teams
        
        # Act
        result = await test_repository.list(limit=10, offset=5)
        
        # Assert
        assert result == teams
        mock_session.execute.assert_called_once()

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_list_all(self, test_repository, mock_database, mock_session):
        """Test listing all entities."""
        # Arrange
        teams = [
            Team(id=1, name="Team 1", country="USA", founded_year=2020),
            Team(id=2, name="Team 2", country="Canada", founded_year=2021)
        ]
        mock_session.execute.return_value.scalars.return_value.all.return_value = teams
        
        # Act
        result = await test_repository.list_all()
        
        # Assert
        assert result == teams
        mock_session.execute.assert_called_once()

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_create_new_entity(self, test_repository, mock_database, mock_session):
        """Test creating new entity."""
        # Arrange
        new_team = Team(name="New Team", country="UK", founded_year=2022)
        # Mock session.get to return None (entity doesn't exist)
        mock_session.get.return_value = None
        
        # Act
        result = await test_repository.create(new_team)
        
        # Assert
        assert result.name == "New Team"
        assert result.country == "UK"
        assert result.founded_year == 2022
        mock_session.add.assert_called_once_with(new_team)
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once_with(new_team)

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_create_entity_with_existing_id(self, test_repository, mock_database, mock_session):
        """Test creating entity with existing ID should fail."""
        # Arrange
        existing_team = Team(id=1, name="Existing Team", country="USA", founded_year=2020)
        new_team = Team(id=1, name="New Team", country="UK", founded_year=2022)
        mock_session.get.return_value = existing_team

        
        # Act & Assert
        with pytest.raises(ValueError, match="Entity with id 1 already exists"):
            await test_repository.create(new_team)
        
        mock_session.add.assert_not_called()
        mock_session.commit.assert_not_called()

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_update_existing_entity(self, test_repository, mock_database, mock_session):
        """Test updating existing entity."""
        # Arrange
        existing_team = Team(id=1, name="Existing Team", country="USA", founded_year=2020)
        updated_data = Team(name="Updated Team", country="Canada", founded_year=2021)
        mock_session.get.return_value = existing_team

        
        # Act
        result = await test_repository.update(1, updated_data)
        
        # Assert
        assert result.id == 1
        assert result.name == "Updated Team"
        assert result.country == "Canada"
        assert result.founded_year == 2021
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_update_non_existing_entity(self, test_repository, mock_database, mock_session):
        """Test updating non-existing entity should fail."""
        # Arrange
        updated_data = Team(name="Updated Team", country="Canada", founded_year=2021)
        mock_session.get.return_value = None

        
        # Act & Assert
        with pytest.raises(ValueError, match="Entity with id 999 not found"):
            await test_repository.update(999, updated_data)
        
        mock_session.add.assert_not_called()
        mock_session.commit.assert_not_called()

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_update_with_mismatched_id(self, test_repository, mock_database, mock_session):
        """Test updating with mismatched ID should fail."""
        # Arrange
        existing_team = Team(id=1, name="Existing Team", country="USA", founded_year=2020)
        updated_data = Team(id=2, name="Updated Team", country="Canada", founded_year=2021)
        mock_session.get.return_value = existing_team

        
        # Act & Assert
        with pytest.raises(ValueError, match="Entity id does not match the requested id"):
            await test_repository.update(1, updated_data)
        
        mock_session.add.assert_not_called()
        mock_session.commit.assert_not_called()

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_delete_existing_entity(self, test_repository, mock_database, mock_session):
        """Test deleting existing entity."""
        # Arrange
        existing_team = Team(id=1, name="Existing Team", country="USA", founded_year=2020)
        mock_session.get.return_value = existing_team

        
        # Act
        await test_repository.delete(1)
        
        # Assert
        mock_session.delete.assert_called_once_with(existing_team)
        mock_session.commit.assert_called_once()

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_delete_non_existing_entity(self, test_repository, mock_database, mock_session):
        """Test deleting non-existing entity."""
        # Arrange
        mock_session.get.return_value = None

        
        # Act
        await test_repository.delete(999)
        
        # Assert
        mock_session.delete.assert_not_called()
        mock_session.commit.assert_not_called()

    def test_repository_initialization(self, test_repository, mock_database):
        """Test repository initialization."""
        # Assert
        assert test_repository.database == mock_database
        assert test_repository.get_model() == Team