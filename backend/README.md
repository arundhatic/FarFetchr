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

---