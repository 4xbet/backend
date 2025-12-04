#!/bin/bash

# Define the base URL for the API gateway
BASE_URL="http://localhost:8000/api"

# Function to log messages
log() {
  echo "[TEST] $1"
}

# 1. Register a new admin user
log "Registering a new admin user..."
ADMIN_EMAIL="admin@example.com"
ADMIN_PASSWORD="password"
curl -X POST "$BASE_URL/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "'$ADMIN_EMAIL'",
    "password": "'$ADMIN_PASSWORD'",
    "role": "admin"
  }' -s -o /dev/null

# 2. Login as the admin user to get a token
log "Logging in as admin..."
TOKEN_RESPONSE=$(curl -X POST "$BASE_URL/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=$ADMIN_EMAIL&password=$ADMIN_PASSWORD")

ACCESS_TOKEN=$(echo $TOKEN_RESPONSE | jq -r .access_token)

if [ "$ACCESS_TOKEN" == "null" ]; then
  log "Failed to get access token. Response: $TOKEN_RESPONSE"
  exit 1
fi

log "Successfully obtained access token."

# 3. Test protected endpoints
log "Testing GET /users/me..."
curl -X GET "$BASE_URL/users/me" -H "Authorization: Bearer $ACCESS_TOKEN"

log "Testing GET /teams/..."
curl -X GET "$BASE_URL/teams/" -H "Authorization: Bearer $ACCESS_TOKEN"

log "Testing GET /matches/..."
curl -X GET "$BASE_URL/matches/" -H "Authorization: Bearer $ACCESS_TOKEN"

log "Testing GET /bets/..."
curl -X GET "$BASE_URL/bets/" -H "Authorization: Bearer $ACCESS_TOKEN"

log "All tests complete."
