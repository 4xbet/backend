#!/bin/bash

BASE_URL="http://localhost:8000/api"
RANDOM_ID=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 8 | head -n 1)
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
USER_EMAIL="user_${RANDOM_ID}@example.com"
RESPONSE=$(curl -s -w "\\n%{http_code}" -X POST "$BASE_URL/users/" \
    -H "Content-Type: application/json" \
    -d "{
        \"email\": \"${USER_EMAIL}\",
        \"password\": \"password\",
        \"role\": \"user\"
    }")
STATUS=$(echo "$RESPONSE" | tail -n1)
check_status $STATUS 200

# 2. Login as user and get token
echo "2. Logging in as user..."
RESPONSE=$(curl -s -w "\\n%{http_code}" -X POST "$BASE_URL/token" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=${USER_EMAIL}&password=password")
STATUS=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')
check_status $STATUS 200
USER_TOKEN=$(echo $BODY | jq -r '.access_token')
if [ -z "$USER_TOKEN" ]; then
    echo "  [FAIL] Could not get user token."
    exit 1
fi
echo "  [SUCCESS] User token obtained."

# 3. Register a new admin
echo "3. Registering new admin..."
ADMIN_EMAIL="admin_${RANDOM_ID}@example.com"
RESPONSE=$(curl -s -w "\\n%{http_code}" -X POST "$BASE_URL/users/" \
    -H "Content-Type: application/json" \
    -d "{
        \"email\": \"${ADMIN_EMAIL}\",
        \"password\": \"adminpassword\",
        \"role\": \"admin\"
    }")
STATUS=$(echo "$RESPONSE" | tail -n1)
check_status $STATUS 200

# 4. Login as admin and get token
echo "4. Logging in as admin..."
RESPONSE=$(curl -s -w "\\n%{http_code}" -X POST "$BASE_URL/token" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=${ADMIN_EMAIL}&password=adminpassword")
STATUS=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')
check_status $STATUS 200
ADMIN_TOKEN=$(echo $BODY | jq -r '.access_token')
if [ -z "$ADMIN_TOKEN" ]; then
    echo "  [FAIL] Could not get admin token."
    exit 1
fi
echo "  [SUCCESS] Admin token obtained."

# 5. Create a team (admin only)
echo "5. Creating a team..."
TEAM_A_NAME="Team A ${RANDOM_ID}"
RESPONSE=$(curl -s -w "\\n%{http_code}" -X POST "$BASE_URL/teams/" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -d "{
        \"name\": \"${TEAM_A_NAME}\",
        \"country\": \"Country A\"
    }")
STATUS=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')
check_status $STATUS 200
TEAM_A_ID=$(echo $BODY | jq -r '.id')
echo "  [SUCCESS] Team created with ID: $TEAM_A_ID"

# 6. Create another team (admin only)
echo "6. Creating another team..."
TEAM_B_NAME="Team B ${RANDOM_ID}"
RESPONSE=$(curl -s -w "\\n%{http_code}" -X POST "$BASE_URL/teams/" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -d "{
        \"name\": \"${TEAM_B_NAME}\",
        \"country\": \"Country B\"
    }")
STATUS=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')
check_status $STATUS 200
TEAM_B_ID=$(echo $BODY | jq -r '.id')
echo "  [SUCCESS] Team created with ID: $TEAM_B_ID"

# 7. Create a match (admin only)
echo "7. Creating a match..."
RESPONSE=$(curl -s -w "\\n%{http_code}" -X POST "$BASE_URL/matches/" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -d "{
        \"home_team_id\": ${TEAM_A_ID},
        \"away_team_id\": ${TEAM_B_ID},
        \"start_time\": \"2024-01-01T12:00:00Z\"
    }")
STATUS=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')
check_status $STATUS 200
MATCH_ID=$(echo $BODY | jq -r '.id')
echo "  [SUCCESS] Match created with ID: $MATCH_ID"

# 8. Create odds for the match (admin only)
echo "8. Creating odds for the match..."
RESPONSE=$(curl -s -w "\\n%{http_code}" -X POST "$BASE_URL/matches/${MATCH_ID}/odds" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -d '{
        "win_home": 1.5,
        "draw": 3.0,
        "win_away": 5.0
    }')
STATUS=$(echo "$RESPONSE" | tail -n1)
check_status $STATUS 200
echo "  [SUCCESS] Odds created."

# 9. Update user wallet
echo "9. Updating user wallet..."
RESPONSE=$(curl -s -w "\\n%{http_code}" -X PATCH "$BASE_URL/users/me/wallet" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $USER_TOKEN" \
    -d '{
        "amount": 100.0
    }')
STATUS=$(echo "$RESPONSE" | tail -n1)
check_status $STATUS 200
echo "  [SUCCESS] User wallet updated."

# 10. Place a bet (user)
echo "10. Placing a bet..."
RESPONSE=$(curl -s -w "\\n%{http_code}" -X POST "$BASE_URL/bets/" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $USER_TOKEN" \
    -d "{
        \"match_id\": ${MATCH_ID},
        \"outcome\": \"win_home\",
        \"amount_staked\": 10.0
    }")
STATUS=$(echo "$RESPONSE" | tail -n1)
check_status $STATUS 200
echo "  [SUCCESS] Bet placed."

echo "--- All tests passed! ---"
