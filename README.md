# FarFetchr: Distance Calculator Web App

## Overview
FarFetchr is a responsive SvelteKit web application that allows users to calculate the distance between two addresses and view their past queries. The app is designed for ease of use, accessibility, and a seamless experience across desktop, tablet, and mobile devices.

## Quick Start: Run the Full App Locally

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd FarFetchr
   ```

2. **Start the backend:**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   # Set up your .env file as described below
   ./setup.sh
   uvicorn main:app --reload
   ```
   The backend will be running at [http://localhost:8000](http://localhost:8000).

3. **Start the frontend:**
   - Open a new terminal window/tab.
   - From the project root:
     ```bash
     npm install
     npm run dev -- --open
     ```
   The frontend will open at [http://localhost:5173](http://localhost:5173).

4. **Test the app:**
   - Visit the frontend URL in your browser.
   - Try calculating distances and viewing history.

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
- **Test Framework:** [Vitest](https://vitest.dev/) is used for unit and component tests. Svelte Testing Library is available for component tests.
- **Test Structure:**
  - Unit tests are located in `tests/unit/` (e.g., `tests/unit/utils.test.ts`).
  - E2E tests are located in `tests/e2e/` (e.g., `tests/e2e/distance-calculator.spec.ts`).
- **How to Run Tests:**
  - Run all unit tests:
    ```bash
    npx vitest run
    ```
  - Run only unit tests:
    ```bash
    npx vitest run tests/unit
    ```
  - Run all E2E tests (requires dev server running at http://localhost:5173):
    ```bash
    npm run dev
    # In a separate terminal:
    npx playwright test
    ```
  - Run E2E tests in headed mode (see browser):
    ```bash
    npx playwright test --headed
    ```
  - Generate and view E2E test report:
    ```bash
    npx playwright show-report
    ```
- **What is Tested:**
  - Utility functions (distance calculation, address validation, cleaning)
  - E2E tests cover:
    - Calculating distance between two addresses
    - Error handling for empty fields, invalid addresses, and identical addresses
    - Viewing historical queries in the history page
    - Geocoding failure (unfindable address)
    - Network error during geocoding
    - Accessibility (labels, roles)
    - Mobile viewport/responsive layout

## E2E Testing
- **Framework:** [Playwright](https://playwright.dev/) is used for end-to-end browser testing.
- **Test Location:** E2E tests are in `tests/e2e/`.
- **How to Run:**
  1. Start the dev server: `npm run dev`
  2. In a separate terminal, run: `npx playwright test`
- **What is Covered:**
  - Main distance calculation flow
  - Error cases (empty, invalid, identical addresses)
  - History page displays previous queries
  - Geocoding failure (unfindable address)
  - Network error during geocoding
  - Accessibility (labels, roles)
  - Mobile viewport/responsive layout

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

---

Enjoy using FarFetchr!
