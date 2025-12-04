#!/bin/bash

# Activate virtual environment
source .venv/bin/activate

# Start user_service
export DATABASE_URL="postgresql+asyncpg://postgres:password@localhost/user_db"
export SECRET_KEY="your_secret_key"
export ROOT_PATH="/api/users"
uvicorn user_service.app.main:app --host 0.0.0.0 --port 8001 > user_service.log 2>&1 &

# Start teams_service
export DATABASE_URL="postgresql+asyncpg://postgres:password@localhost/teams_db"
export SECRET_KEY="your_secret_key"
export ROOT_PATH="/api/teams"
uvicorn teams_service.app.main:app --host 0.0.0.0 --port 8002 > teams_service.log 2>&1 &

# Start matches_service
export DATABASE_URL="postgresql+asyncpg://postgres:password@localhost/matches_db"
export SECRET_KEY="your_secret_key"
export ROOT_PATH="/api/matches"
uvicorn matches_service.app.main:app --host 0.0.0.0 --port 8003 > matches_service.log 2>&1 &

# Start bets_service
export DATABASE_URL="postgresql+asyncpg://postgres:password@localhost/bets_db"
export SECRET_KEY="your_secret_key"
export USER_SERVICE_URL="http://localhost:8001"
export MATCHES_SERVICE_URL="http://localhost:8003"
export ROOT_PATH="/api/bets"
uvicorn bets_service.app.main:app --host 0.0.0.0 --port 8004 > bets_service.log 2>&1 &

echo "All services are starting..."
sleep 10 # Give services time to start
jobs
