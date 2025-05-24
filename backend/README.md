# FarFetchr Backend (FastAPI)

This is the backend REST API for the FarFetchr distance calculator app. It provides endpoints to calculate distances between addresses (using Nominatim for geocoding) and stores/retrieves past queries in a PostgreSQL database.

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

---