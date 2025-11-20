#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Install PostgreSQL ---
echo "Installing PostgreSQL..."
sudo apt-get update
sudo apt-get install -y postgresql
sudo service postgresql start

# --- Configure PostgreSQL ---
echo "Configuring PostgreSQL..."
sudo -u postgres psql -c "CREATE DATABASE user_db;"
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE user_db TO postgres;"
sudo -u postgres psql -c "CREATE DATABASE teams_db;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE teams_db TO postgres;"
sudo -u postgres psql -c "CREATE DATABASE matches_db;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE matches_db TO postgres;"
sudo -u postgres psql -c "CREATE DATABASE bets_db;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE bets_db TO postgres;"

# --- Install Nginx ---
echo "Installing Nginx..."
sudo apt-get install -y nginx

# --- Configure Nginx ---
echo "Configuring Nginx..."
sudo cp api_gateway/nginx.conf /etc/nginx/nginx.conf

# --- Create Python virtual environment ---
echo "Creating Python virtual environment..."
python3 -m venv .venv

# --- Install Python dependencies ---
echo "Installing Python dependencies..."
source .venv/bin/activate
pip install --upgrade pip
cat user_service/requirements.txt teams_service/requirements.txt matches_service/requirements.txt bets_service/requirements.txt > temp_requirements.txt
pip install -r temp_requirements.txt
rm temp_requirements.txt

echo "Setup complete!"
