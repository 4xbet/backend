#!/bin/bash

sudo apt-get install -y postgresql
sudo service postgresql start
sudo -u postgres psql -c "CREATE DATABASE user_db;"
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE user_db TO postgres;"
sudo -u postgres psql -c "CREATE DATABASE teams_db;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE teams_db TO postgres;"
sudo -u postgres psql -c "CREATE DATABASE matches_db;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE matches_db TO postgres;"