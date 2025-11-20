# Local Backend Setup Guide

This guide explains how to set up and run the entire backend application locally, without using Docker.

## Prerequisites

- An Ubuntu-based environment (tested on Ubuntu 24.04).
- `python3` and `python3-venv` installed.
- `curl` installed.

## 1. Setup

This step installs and configures all the necessary services (PostgreSQL, Nginx) and the Python environment.

**Important:** This script uses `sudo` and will install packages on your system. Please review the script before running it.

To run the setup, execute the following command from the root of the repository:

```bash
./setup_local_backend.sh
```

This script will:
1.  Install PostgreSQL and start the service.
2.  Create the four required databases (`user_db`, `teams_db`, `matches_db`, `bets_db`).
3.  Set the password for the `postgres` user to `password`.
4.  Install and configure Nginx as a reverse proxy.
5.  Create a Python virtual environment in `.venv/`.
6.  Install all required Python dependencies into the virtual environment.

## 2. Start the Backend

After the setup is complete, you can start all the backend services.

To start the services, run the following command from the root of the repository:

```bash
./start_local_backend.sh
```

This script will:
1.  Start the Nginx service.
2.  Activate the Python virtual environment.
3.  Start the four FastAPI microservices (`user_service`, `teams_service`, `matches_service`, `bets_service`) in the background on ports 8001-8004.

The API gateway will be available at `http://localhost:8000`.

## 3. Stop the Backend

To stop all the running backend services, you can run the following command:

```bash
pkill -f uvicorn && sudo service nginx stop
```
