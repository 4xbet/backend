#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Start Nginx ---
echo "Starting Nginx..."
sudo service nginx start

# --- Activate virtual environment ---
source .venv/bin/activate

# --- Start FastAPI services ---
echo "Starting FastAPI services..."
export SECRET_KEY="your_secret_key" # This can be centralized

# Start user_service
export DATABASE_URL="postgresql+asyncpg://postgres:password@localhost/user_db"
export ROOT_PATH="/api/users"
uvicorn user_service.app.main:app --host 0.0.0.0 --port 8001 > user_service.log 2>&1 &

# Start teams_service
export DATABASE_URL="postgresql+asyncpg://postgres:password@localhost/teams_db"
export ROOT_PATH="/api/teams"
uvicorn teams_service.app.main:app --host 0.0.0.0 --port 8002 > teams_service.log 2>&1 &

# Start matches_service
export DATABASE_URL="postgresql+asyncpg://postgres:password@localhost/matches_db"
export ROOT_PATH="/api/matches"
uvicorn matches_service.app.main:app --host 0.0.0.0 --port 8003 > matches_service.log 2>&1 &

# Start bets_service
export DATABASE_URL="postgresql+asyncpg://postgres:password@localhost/bets_db"
export USER_SERVICE_URL="http://localhost:8001"
export MATCHES_SERVICE_URL="http://localhost:8003"
export ROOT_PATH="/api/bets"
uvicorn bets_service.app.main:app --host 0.0.0.0 --port 8004 > bets_service.log 2>&1 &

echo "Backend services are starting in the background. Check logs for status."
echo "To stop all services, run: pkill -f uvicorn && sudo service nginx stop"
