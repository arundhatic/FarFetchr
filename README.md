# FarFetchr: Distance Calculator Web App

---

## Project Highlights

- **Robust local development with Docker Compose.**
- **Secure, environment-variable-based configuration.**
- **Automated database initialization.**
- **Production-ready cloud deployment (Vercel + Render).**
- **Live, public URLs:**
  - Frontend: [https://far-fetchr.vercel.app/](https://far-fetchr.vercel.app/)
  - Backend API docs: [https://farfetchr-backend.onrender.com/docs](https://farfetchr-backend.onrender.com/docs)

---

## Quick Start: Fullstack with Docker Compose

1. **Build and start everything:**
   ```bash
   docker-compose up --build
   ```
   - Frontend: http://localhost:4173
   - Backend: http://localhost:8000
   - Database: persists in Docker volume `pgdata`

2. **Reset the database (start fresh):**
   ```bash
   docker-compose down -v
   docker-compose up --build
   ```
   This will remove all data and reinitialize the DB.

3. **Connect to the database with DBeaver or any other database client:**
   - Host: `localhost`
   - Port: `5432`
   - Database: `farfetchr`
   - User: `postgres`
   - Password: `<your_postgres_password>`
   > The default password is set in your `docker-compose.yml` as `POSTGRES_PASSWORD`. Change it as needed for your environment.
   > Ensure your local Postgres is stopped to avoid port conflicts.

4. **No manual DB initialization needed!**
   - The backend automatically creates tables on startup.

5. **Troubleshooting:**
   - If you see old data after restart, use `docker-compose down -v` to clear the DB.
   - If you get connection errors, ensure no other service is using port 5432.

## Environment Setup

1. Copy the example environment files and fill in your own values:
   ```bash
   cp .env.example .env
   cp backend/.env.example backend/.env
   ```
2. Edit `.env` and `backend/.env` to set your own secrets and configuration.
3. **Do NOT commit your real `.env` files to git.** Only commit the `.env.example` files as templates.

---

## Advanced/Manual Development (Optional)

If you want to run backend and frontend locally (not recommended for most users):

1. **Backend:**
   - Set up Python venv, install requirements, configure `.env`, and run `uvicorn main:app --reload` as before.
2. **Frontend:**
   - Run `npm install` and `npm run dev` as before.

> **Note:** You must manually initialize the DB if not using Docker Compose.

## Features
- **Distance Calculation:** Enter a source and destination address to calculate the distance in miles, kilometers, or both.
- **Geocoding:** Uses OpenStreetMap Nominatim to convert addresses to coordinates.
- **Error Handling:** Robust validation and user-friendly error messages for invalid or missing addresses, network issues, and geocoding failures.
- **Query History:** Stores the last 20 successful queries in the browser's local storage. View historical queries in a sortable table.
- **Responsive Design:** Fully adapts to all screen sizes, ensuring usability on desktops, tablets, and smartphones.
- **Accessible UI:** Proper label associations, keyboard navigation, and color contrast.
- **Modern UX:** Loading spinners, animated error toasts, and Figma-matching design.

## Use Cases
- Quickly find the driving or straight-line distance between two addresses for travel, logistics, or planning.
- Keep a record of recent distance queries for reference or reporting.
- Use on any device, from desktop to mobile, without loss of functionality.

## Error Checks & Validation
- **Empty Fields:** Prompts user to fill both source and destination.
- **Invalid Format:** Detects addresses that are too short, all numbers, no letters, or only special characters.
- **Identical Addresses:** Prevents calculation if source and destination are the same.
- **Geocoding Failure:** Informs user if the address cannot be found.
- **Network/API Errors:** Notifies user of connectivity issues.
- **All errors are shown in a styled toast notification at the bottom right.**
- **For a full list of error conditions and validation logic, see [`tests/README.md`](tests/README.md).**

## How It Works
- **Main Page:**
  - Enter addresses, select unit, and click "Calculate Distance".
  - The app geocodes both addresses, calculates the distance, and displays the result.
  - Each successful calculation is saved to history.
  - Errors are shown in a toast notification.
- **View Historical Queries:**
  - Click the "View Historical Queries" button to see a table of past queries.
  - Table includes source, destination, and distances in both units.
  - Click "Back to Calculator" to return to the main page.

## Technologies Used
- [SvelteKit](https://kit.svelte.dev/)
- [OpenStreetMap Nominatim API](https://nominatim.openstreetmap.org/)
- TypeScript, HTML, CSS

## Testing

- **Unit tests:**
  ```bash
  npm run test:unit
  ```

- **End-to-End (E2E) tests (Docker Compose):**
  Make sure the full stack is running with Docker Compose (`docker-compose up --build`), then run:
  ```bash
  npm run test:e2e:docker
  ```
  This will run Playwright E2E tests against the frontend at `http://localhost:4173`.

> The previous `npm run test:e2e` script for local dev has been removed to avoid environment conflicts.

## Notes

* Data is now stored and retrieved via a FastAPI + PostgreSQL backend.
* The app is for demonstration and prototyping purposes.
* For production use, consider adding authentication, rate limiting, and API keys.

## Backend Setup

To set up and run the FastAPI backend:

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```
2. **Create and activate a Python virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up your PostgreSQL database:**
   - Make sure PostgreSQL is running.
   - Create a database (e.g., `farfetchr`).
   - Create a user/role with access to the database.
5. **Configure environment variables:**
   - Create a `.env` file in the `backend/` directory with:
     ```
     DATABASE_URL=postgresql+asyncpg://<username>:<password>@localhost:5432/farfetchr
     ```
     Replace `<username>` and `<password>` with your PostgreSQL credentials.
6. **Initialize the database tables:**
   ```bash
   ./setup.sh
   ```
   (This will create tables and install dependencies if needed.)
7. **Run the FastAPI server:**
   ```bash
   uvicorn main:app --reload
   ```
   The backend will be available at `http://localhost:8000`.

### Test Scripts (from package.json)

You can use the following npm scripts for testing:

- `npm run test:unit` — Runs all unit tests in `tests/unit` using Vitest
- `npm run test:e2e` — Runs all Playwright E2E tests in `tests/e2e`
- `npm test` — Runs both unit and E2E tests in sequence

### Backend Test Script

To run all backend tests from the backend folder, use:
```bash
cd backend
./run_tests.sh
```
See backend/README.md for more details.

## Running Frontend and Backend in Docker (with Host Database)

You can run both the frontend and backend in Docker containers, while using your local PostgreSQL database.

### 1. Start your local PostgreSQL database
- Ensure your database is running and accessible at `localhost:5432`
- The database `farfetchr` and user/password `postgres:grid2home` should exist

### 2. Build and run the backend Docker container (from backend directory)
```bash
cd backend
./run_docker.sh .env.docker
```

### 3. Build and run the frontend Docker container (from project root)
```bash
docker build -t farfetchr-frontend .
docker run -p 4173:4173 farfetchr-frontend
```

### 4. Access the app
- Frontend: http://localhost:4173
- Backend: http://localhost:8000
- API docs: http://localhost:8000/docs

---

## Running the App: Local, Docker Compose, and Manual

### 1. Local Development (manual, with host DB)
- Backend: uses `backend/.env` with `localhost` for DB
- Frontend: runs with Vite/SvelteKit dev server

```bash
# Start PostgreSQL locally (if not already running)
# Start backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
# In a new terminal, start frontend
cd ..
npm install
npm run dev
```

### 2. Full Stack with Docker Compose
- Runs Postgres, backend, and frontend as containers
- Backend connects to DB at `db:5432`

```bash
docker-compose up --build
```
- Frontend: http://localhost:4173
- Backend: http://localhost:8000
- DB: localhost:5432 (exposed for dev)

---

## Running the Frontend in Docker

To build and run the frontend as a Docker container:

```bash
docker build -t farfetchr-frontend .
docker run -p 4173:4173 farfetchr-frontend
```

The app will be available at http://localhost:4173

---

## Troubleshooting

### 1. Database Connection Issues
- **Error:** `connection refused` or `database does not exist`
  - Make sure Docker is running and the database container is healthy.
  - Ensure no other service (like local Postgres) is using port 5432, or stop it before running Docker Compose.
  - Use `docker-compose ps` to check container status.

### 2. Data Not Reset After Restart
- **Symptom:** Old data appears after `docker-compose down` and `up`
  - Use `docker-compose down -v` to remove the persistent database volume and start fresh.

### 3. DBeaver Shows Old Data
- Make sure you are connecting to the Dockerized Postgres, not your local Postgres.
- Stop your local Postgres service before connecting to `localhost:5432` in DBeaver.

### 4. Port Conflicts
- If you get errors about port 5432 or 8000/4173 being in use, stop any other services using those ports or change the port mapping in `docker-compose.yml`.

### 5. Backend or Frontend Not Starting
- Check logs with `docker-compose logs backend` or `docker-compose logs frontend` for error messages.
- Make sure all dependencies are installed and Docker images are rebuilt after changes.

### 6. Database Tables Missing
- The backend automatically creates tables on startup. If tables are missing, check backend logs for errors.

### 7. Playwright/E2E Test Failures
- Ensure the frontend and backend are running at the expected URLs.
- If using Docker Compose, update test URLs to match (`http://localhost:4173` for frontend).

Enjoy using FarFetchr!

## Future Features

* **Authentication:**
  - Allow users to create accounts and log in securely.
  - Each user will have a private, persistent history of their distance queries, accessible from any device.

* **Export History:**
  - Users will be able to export their query history as CSV or PDF files.

* **Map Visualization:**
  - Display calculated routes or points directly on an interactive map (using Leaflet, Mapbox, or similar).

* **Caching:**
  - Implement caching for frequent or repeated queries to improve performance and reduce API usage.
  - Results for common address pairs will be served instantly.
  - Reduces load on external geocoding and routing services, and speeds up the user experience.
