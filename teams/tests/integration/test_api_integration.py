import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from main import app 
from src.db.models import Team, Athlete


@pytest.mark.integration
class TestApiIntegration:
    """Integration tests for the API endpoints with a real database and client."""

    @pytest.mark.asyncio
    async def test_teams_api_flow(self, async_client: AsyncClient, sample_team_in_db: Team):
        """Test the full CRUD flow for the /teams API endpoint."""
        team_data = {
            "name": "API Flow Team",
            "country": "APILand",
            "founded_year": 2022
        }
        response = await async_client.post("/teams/", json=team_data)
        assert response.status_code == 201
        created_team = response.json()
        assert created_team["name"] == "API Flow Team"
        team_id = created_team["id"]

        response = await async_client.get(f"/teams/{team_id}")
        assert response.status_code == 200
        assert response.json()["name"] == "API Flow Team"

        update_data = {"city": "API City"}
        response = await async_client.put(f"/teams/{team_id}", json=update_data)
        assert response.status_code == 200
        assert response.json()["city"] == "API City"

        response = await async_client.get("/teams/")
        assert response.status_code == 200
        assert len(response.json()) >= 1

        response = await async_client.delete(f"/teams/{team_id}")
        assert response.status_code == 204

        response = await async_client.get(f"/teams/{team_id}")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_athletes_api_flow(self, async_client: AsyncClient, sample_team_in_db: Team):
        """Test the full CRUD flow for the /athletes API endpoint."""
        athlete_data = {
            "first_name": "API",
            "last_name": "Athlete",
            "date_of_birth": "2003-03-03",
            "position": "Striker",
            "team_id": sample_team_in_db.id
        }
        response = await async_client.post("/athletes/", json=athlete_data)
        assert response.status_code == 201
        created_athlete = response.json()
        assert created_athlete["first_name"] == "API"
        athlete_id = created_athlete["id"]

        response = await async_client.get(f"/athletes/{athlete_id}")
        assert response.status_code == 200
        assert response.json()["last_name"] == "Athlete"

        update_data = {"position": "Winger"}
        response = await async_client.put(f"/athletes/{athlete_id}", json=update_data)
        assert response.status_code == 200
        assert response.json()["position"] == "Winger"

        response = await async_client.get("/athletes/")
        assert response.status_code == 200
        assert len(response.json()) >= 1

        response = await async_client.delete(f"/athletes/{athlete_id}")
        assert response.status_code == 204

        response = await async_client.get(f"/athletes/{athlete_id}")
        assert response.status_code == 404
