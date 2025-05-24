# FarFetchr Backend (FastAPI)

## Quick Start: Docker Compose (Recommended)

- The backend is started and initialized automatically via Docker Compose.
- No manual DB initialization is needed; tables are created on container startup.

To start the backend (and full stack):
```bash
docker-compose up --build
```
- Backend: http://localhost:8000
- Database: persists in Docker volume `pgdata`

To reset the database (start fresh):
```bash
docker-compose down -v
```

## Environment Setup

1. Copy the example environment file and fill in your own values:
   ```bash
   cp backend/.env.example backend/.env
   ```
2. Edit `backend/.env` to set your own secrets and configuration.
3. **Do NOT commit your real `.env` files to git.** Only commit the `.env.example` file as a template.

---

## Advanced/Manual Development (Optional)

If you want to run the backend locally (not recommended for most users):
1. Set up Python venv, install requirements, configure `.env`, and run `uvicorn main:app --reload` as before.
2. You must manually initialize the DB if not using Docker Compose.

---

## Features
- REST API to calculate distance between two addresses
- Geocoding using Nominatim API
- Stores all queries in PostgreSQL
- Retrieve query history
- Robust error handling

## Tech Stack
- Python 3
- FastAPI
- PostgreSQL
- SQLAlchemy
- httpx
- Pydantic

## Project Structure
```
backend/
  ├── main.py         # FastAPI entry point and API routes
  ├── models.py       # SQLAlchemy ORM models
  ├── schemas.py      # Pydantic request/response schemas
  ├── database.py     # Database connection and session
  ├── utils.py        # Utility functions (geocoding, haversine, etc.)
  ├── .env            # Environment variables (DB credentials, etc.)
  ├── requirements.txt
  └── venv/           # Python virtual environment
```

## Setup
1. Create and activate a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your PostgreSQL database and add credentials to `.env` (see example below).
4. Run the FastAPI app:
   ```bash
   uvicorn main:app --reload
   ```

## .env Example
```
DATABASE_URL=postgresql+asyncpg://<username>:<password>@localhost:5432/farfetchr
```

## Running Backend Tests

1. Create and activate a Python virtual environment (if not already):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install all dependencies (including test dependencies):
   ```bash
   pip install -r requirements.txt
   ```
3. Run all backend tests (unit and API/integration) from the backend directory:
   ```bash
   pytest tests
   ```

All test dependencies are included in `requirements.txt`.

**Troubleshooting:**
- If you see import errors (e.g., `ModuleNotFoundError`), make sure you are running the tests from the `backend` directory and that your virtual environment is activated.

### Running Backend Tests with a Script

You can use the provided shell script to run all backend tests easily:

1. Make sure you are in the backend directory:
   ```bash
   cd backend
   ```
2. Make the script executable (only needed once):
   ```bash
   chmod +x run_tests.sh
   ```
3. Run all backend tests:
   ```bash
   ./run_tests.sh
   ```

This will activate the virtual environment and run all backend tests with pytest.

### Running Backend in Docker with Host Database

To run the backend in Docker and connect to your local PostgreSQL database:

```bash
./run_docker.sh .env.docker
```

This uses the `backend/.env.docker` file, which should have:
```
DATABASE_URL=postgresql+asyncpg://postgres:grid2home@host.docker.internal:5432/farfetchr
```

## Running Backend in Docker with Local DB (manual)

To run the backend in Docker and connect to a local database (using `localhost`):

```bash
./run_docker.sh
```

This uses the `backend/.env` file, which should have:
```
DATABASE_URL=postgresql+asyncpg://postgres:grid2home@localhost:5432/farfetchr
```

---

## Troubleshooting

### 1. Database Connection Issues
- **Error:** `connection refused` or `database does not exist`
  - Make sure Docker is running and the database container is healthy.
  - Ensure no other service (like local Postgres) is using port 5432, or stop it before running Docker Compose.
  - Use `docker-compose ps` to check container status.

### 2. Data Not Reset After Restart
- **Symptom:** Old data appears after `docker-compose down` and `up`
  - Use `