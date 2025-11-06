import pytest
from datetime import date
from sqlalchemy import inspect
from src.db.models import Team, Athlete, Base


@pytest.mark.unit
class TestTeamModel:
    """Unit tests for Team model."""

    def test_team_model_structure(self):
        """Test that Team model has all required columns."""
        # Arrange
        mapper = inspect(Team)
        
        # Act & Assert
        assert hasattr(Team, '__tablename__')
        assert Team.__tablename__ == 'teams'
        
        # Check columns
        columns = mapper.columns
        expected_columns = ['id', 'name', 'country', 'city', 'founded_year', 'logo_url']
        for col in expected_columns:
            assert col in columns
        
        # Check column types and constraints
        assert columns['id'].primary_key is True
        assert columns['name'].unique is True
        assert columns['name'].nullable is False
        assert columns['country'].nullable is False
        assert columns['founded_year'].nullable is False
        assert columns['city'].nullable is True
        assert columns['logo_url'].nullable is True

    def test_team_creation(self):
        """Test creating a Team instance."""
        # Arrange & Act
        team = Team(
            name="Test Team",
            country="USA",
            city="New York",
            founded_year=2020,
            logo_url="https://example.com/logo.png"
        )
        
        # Assert
        assert team.name == "Test Team"
        assert team.country == "USA"
        assert team.city == "New York"
        assert team.founded_year == 2020
        assert team.logo_url == "https://example.com/logo.png"
        assert team.athletes == []

    def test_team_repr(self):
        """Test Team string representation."""
        # Arrange
        team = Team(
            name="Test Team",
            country="USA",
            founded_year=2020
        )
        
        # Act & Assert
        assert str(team) == "<Team(id=None, name='Test Team', country='USA')>"

    def test_team_with_id(self):
        """Test Team with assigned ID."""
        # Arrange
        team = Team(
            id=1,
            name="Test Team",
            country="USA",
            founded_year=2020
        )
        
        # Act & Assert
        assert team.id == 1
        assert str(team) == "<Team(id=1, name='Test Team', country='USA')>"


@pytest.mark.unit
class TestAthleteModel:
    """Unit tests for Athlete model."""

    def test_athlete_model_structure(self):
        """Test that Athlete model has all required columns."""
        # Arrange
        mapper = inspect(Athlete)
        
        # Act & Assert
        assert hasattr(Athlete, '__tablename__')
        assert Athlete.__tablename__ == 'athletes'
        
        # Check columns
        columns = mapper.columns
        expected_columns = ['id', 'first_name', 'last_name', 'date_of_birth', 'position', 'team_id']
        for col in expected_columns:
            assert col in columns
        
        # Check column types and constraints
        assert columns['id'].primary_key is True
        assert columns['first_name'].nullable is False
        assert columns['last_name'].nullable is False
        assert columns['date_of_birth'].nullable is False
        assert columns['position'].nullable is False
        assert columns['team_id'].nullable is False

    def test_athlete_creation(self):
        """Test creating an Athlete instance."""
        # Arrange & Act
        athlete = Athlete(
            first_name="John",
            last_name="Doe",
            date_of_birth=date(2000, 1, 1),
            position="Forward",
            team_id=1
        )
        
        # Assert
        assert athlete.first_name == "John"
        assert athlete.last_name == "Doe"
        assert athlete.date_of_birth == date(2000, 1, 1)
        assert athlete.position == "Forward"
        assert athlete.team_id == 1
        assert athlete.team is None

    def test_athlete_repr(self):
        """Test Athlete string representation."""
        # Arrange
        athlete = Athlete(
            first_name="John",
            last_name="Doe",
            date_of_birth=date(2000, 1, 1),
            position="Forward",
            team_id=1
        )
        
        # Act & Assert
        assert str(athlete) == "<Athlete(id=None, name='John Doe', position='Forward')>"

    def test_athlete_with_id(self):
        """Test Athlete with assigned ID."""
        # Arrange
        athlete = Athlete(
            id=1,
            first_name="John",
            last_name="Doe",
            date_of_birth=date(2000, 1, 1),
            position="Forward",
            team_id=1
        )
        
        # Act & Assert
        assert athlete.id == 1
        assert str(athlete) == "<Athlete(id=1, name='John Doe', position='Forward')>"

    def test_athlete_full_name_property(self):
        """Test athlete full name property."""
        # Arrange
        athlete = Athlete(
            first_name="John",
            last_name="Doe",
            date_of_birth=date(2000, 1, 1),
            position="Forward",
            team_id=1
        )
        
        # Act & Assert
        assert athlete.name == "John Doe"


@pytest.mark.unit
class TestModelRelationships:
    """Unit tests for model relationships."""

    def test_team_athletes_relationship(self):
        """Test Team-Athletes relationship."""
        # Arrange
        team = Team(
            name="Test Team",
            country="USA",
            founded_year=2020
        )
        athlete1 = Athlete(
            first_name="John",
            last_name="Doe",
            date_of_birth=date(2000, 1, 1),
            position="Forward",
            team_id=1
        )
        athlete2 = Athlete(
            first_name="Jane",
            last_name="Smith",
            date_of_birth=date(2001, 2, 15),
            position="Defender",
            team_id=1
        )
        
        # Act
        team.athletes = [athlete1, athlete2]
        athlete1.team = team
        athlete2.team = team
        
        # Assert
        assert len(team.athletes) == 2
        assert athlete1.team == team
        assert athlete2.team == team
        assert team.athletes[0] == athlete1
        assert team.athletes[1] == athlete2

    def test_athlete_team_relationship(self):
        """Test Athlete-Team relationship."""
        # Arrange
        team = Team(
            name="Test Team",
            country="USA",
            founded_year=2020
        )
        athlete = Athlete(
            first_name="John",
            last_name="Doe",
            date_of_birth=date(2000, 1, 1),
            position="Forward",
            team_id=1
        )
        
        # Act
        athlete.team = team
        
        # Assert
        assert athlete.team == team

    def test_cascade_delete_relationship(self):
        """Test that cascade delete is properly configured."""
        # Arrange
        mapper = inspect(Team)
        
        # Act
        athletes_relationship = mapper.relationships.get('athletes')
        
        # Assert
        assert athletes_relationship is not None
        assert 'delete-orphan' in str(athletes_relationship.cascade)
        assert 'delete' in str(athletes_relationship.cascade)