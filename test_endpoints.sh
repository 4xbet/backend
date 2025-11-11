#!/bin/bash

BASE_URL="http://localhost:8000/api"
JQ_PATH=$(which jq)

if [ -z "$JQ_PATH" ]; then
    echo "jq is not installed. Please install jq to run this script."
    exit 1
fi

function check_status {
    if [ "$1" -ne "$2" ]; then
        echo "  [FAIL] Expected status $2, but got $1."
        exit 1
    else
        echo "  [SUCCESS] Received status $1."
    fi
}

echo "--- Running Endpoint Tests ---"

# 1. Register a new user
echo "1. Registering new user..."
STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE_URL/users/" \
    -H "Content-Type: application/json" \
    -d '{
        "email": "user@example.com",
        "password": "password",
        "role": "user"
    }')
check_status $STATUS 200

# 2. Login as user and get token
echo "2. Logging in as user..."
RESPONSE=$(curl -s -X POST "$BASE_URL/token" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=user@example.com&password=password")
USER_TOKEN=$(echo $RESPONSE | jq -r '.access_token')
check_status $(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE_URL/token" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=user@example.com&password=password") 200

if [ -z "$USER_TOKEN" ]; then
    echo "  [FAIL] Could not get user token."
    exit 1
fi
echo "  [SUCCESS] User token obtained."

# 3. Register a new admin
echo "3. Registering new admin..."
STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE_URL/users/" \
    -H "Content-Type: application/json" \
    -d '{
        "email": "admin@example.com",
        "password": "adminpassword",
        "role": "admin"
    }')
check_status $STATUS 200

# 4. Login as admin and get token
echo "4. Logging in as admin..."
RESPONSE=$(curl -s -X POST "$BASE_URL/token" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=admin@example.com&password=adminpassword")
ADMIN_TOKEN=$(echo $RESPONSE | jq -r '.access_token')
check_status $(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE_URL/token" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=admin@example.com&password=adminpassword") 200

if [ -z "$ADMIN_TOKEN" ]; then
    echo "  [FAIL] Could not get admin token."
    exit 1
fi
echo "  [SUCCESS] Admin token obtained."

# 5. Create a team (admin only)
echo "5. Creating a team..."
STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE_URL/teams/" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -d '{
        "name": "Team A",
        "country": "Country A"
    }')
check_status $STATUS 200
echo "  [SUCCESS] Team created."

# 6. Create a match (admin only)
echo "6. Creating a match..."
STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE_URL/matches/" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -d '{
        "home_team_id": 1,
        "away_team_id": 2,
        "start_time": "2024-01-01T12:00:00"
    }')
check_status $STATUS 200
echo "  [SUCCESS] Match created."

# 7. Place a bet (user)
echo "7. Placing a bet..."
STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE_URL/bets/" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $USER_TOKEN" \
    -d '{
        "match_id": 1,
        "outcome": "win_home",
        "amount_staked": 10.0
    }')
check_status $STATUS 200
echo "  [SUCCESS] Bet placed."

echo "--- All tests passed! ---"
