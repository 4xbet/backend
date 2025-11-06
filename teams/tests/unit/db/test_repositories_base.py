import pytest
from unittest.mock import Mock, AsyncMock
from src.db.repositories.base import BaseRepository
from src.db.models import Team

class TestBaseRepository:
    """Unit tests for BaseRepository."""

    @pytest.fixture
    def mock_session(self):
        """Create mock database session."""
        session = AsyncMock()
        
        # Set up the proper mock chain for execute().scalars().first()/all()
        mock_result = Mock()
        mock_scalars = Mock()
        
        session.execute = AsyncMock(return_value=mock_result)
        mock_result.scalars = Mock(return_value=mock_scalars)
        mock_scalars.first = Mock(return_value=None)
        mock_scalars.all = Mock(return_value=[])
        
        session.get = AsyncMock()
        session.add = Mock()
        session.delete = AsyncMock()
        session.commit = AsyncMock()
        session.refresh = AsyncMock()
        session.close = AsyncMock()
        
        return session

    @pytest.fixture
    def test_repository(self, mock_session):
        """Create test repository implementation."""
        class TestRepository(BaseRepository[Team]):
            def get_model(self):
                return Team
        return TestRepository(mock_session)

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_get_existing_entity(self, test_repository, mock_session):
        """Test getting existing entity."""
        expected_team = Team(id=1, name="Test Team", country="USA", founded_year=2020)
        mock_session.execute.return_value.scalars.return_value.first.return_value = expected_team
        
        result = await test_repository.get(1)
        
        assert result == expected_team
        mock_session.execute.assert_called_once()
        mock_session.commit.assert_not_called()

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_get_non_existing_entity(self, test_repository, mock_session):
        """Test getting non-existing entity."""
        mock_session.execute.return_value.scalars.return_value.first.return_value = None
        
        result = await test_repository.get(999)
        
        assert result is None
        mock_session.execute.assert_called_once()

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_list_with_limit_offset(self, test_repository, mock_session):
        """Test listing entities with limit and offset."""
        teams = [
            Team(id=1, name="Team 1", country="USA", founded_year=2020),
            Team(id=2, name="Team 2", country="Canada", founded_year=2021)
        ]
        mock_session.execute.return_value.scalars.return_value.all.return_value = teams
        
        result = await test_repository.list(limit=10, offset=5)
        
        assert result == teams
        mock_session.execute.assert_called_once()

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_list_all(self, test_repository, mock_session):
        """Test listing all entities."""
        teams = [
            Team(id=1, name="Team 1", country="USA", founded_year=2020),
            Team(id=2, name="Team 2", country="Canada", founded_year=2021)
        ]
        mock_session.execute.return_value.scalars.return_value.all.return_value = teams
        
        result = await test_repository.list_all()
        
        assert result == teams
        mock_session.execute.assert_called_once()

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_create_new_entity(self, test_repository, mock_session):
        """Test creating new entity."""
        new_team = Team(name="New Team", country="UK", founded_year=2022)
        mock_session.get.return_value = None
        
        result = await test_repository.create(new_team)
        
        assert result.name == "New Team"
        mock_session.add.assert_called_once_with(new_team)
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once_with(new_team)

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_create_entity_with_existing_id(self, test_repository, mock_session):
        """Test creating entity with existing ID should fail."""
        existing_team = Team(id=1, name="Existing Team", country="USA", founded_year=2020)
        new_team = Team(id=1, name="New Team", country="UK", founded_year=2022)
        mock_session.get.return_value = existing_team

        with pytest.raises(ValueError, match="Entity with id 1 already exists"):
            await test_repository.create(new_team)
        
        mock_session.add.assert_not_called()
        mock_session.commit.assert_not_called()

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_update_existing_entity(self, test_repository, mock_session):
        """Test updating existing entity."""
        existing_team = Team(id=1, name="Existing Team", country="USA", founded_year=2020)
        updated_data = Team(name="Updated Team", country="Canada", founded_year=2021)
        mock_session.get.return_value = existing_team

        result = await test_repository.update(1, updated_data)
        
        assert result.id == 1
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_update_non_existing_entity(self, test_repository, mock_session):
        """Test updating non-existing entity should fail."""
        updated_data = Team(name="Updated Team", country="Canada", founded_year=2021)
        mock_session.get.return_value = None

        with pytest.raises(ValueError, match="Entity with id 999 not found"):
            await test_repository.update(999, updated_data)
        
        mock_session.add.assert_not_called()
        mock_session.commit.assert_not_called()

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_update_with_mismatched_id(self, test_repository, mock_session):
        """Test updating with mismatched ID should fail."""
        existing_team = Team(id=1, name="Existing Team", country="USA", founded_year=2020)
        updated_data = Team(id=2, name="Updated Team", country="Canada", founded_year=2021)
        mock_session.get.return_value = existing_team

        with pytest.raises(ValueError, match="Entity id does not match the requested id"):
            await test_repository.update(1, updated_data)
        
        mock_session.add.assert_not_called()
        mock_session.commit.assert_not_called()

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_delete_existing_entity(self, test_repository, mock_session):
        """Test deleting existing entity."""
        existing_team = Team(id=1, name="Existing Team", country="USA", founded_year=2020)
        mock_session.get.return_value = existing_team
        
        await test_repository.delete(1)
        
        mock_session.delete.assert_called_once_with(existing_team)
        mock_session.commit.assert_called_once()

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_delete_non_existing_entity(self, test_repository, mock_session):
        """Test deleting non-existing entity."""
        mock_session.get.return_value = None
        
        await test_repository.delete(999)
        
        mock_session.delete.assert_not_called()
        mock_session.commit.assert_not_called()

    def test_repository_initialization(self, test_repository, mock_session):
        """Test repository initialization."""
        assert test_repository.session == mock_session
        assert test_repository.get_model() == Team
