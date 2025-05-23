# Test README: Error Conditions for Calculate Distance

This document describes all error conditions and validation logic for the **Calculate Distance** feature in the FarFetchr app, as covered by both frontend and backend code and tests.

---

## Frontend Error Conditions (SvelteKit UI)

1. **Empty Fields**
   - Either source or destination address is empty.

2. **Invalid Address Format (Stricter Validation)**
   - Address is less than 8 characters.
   - Address does not contain at least one number (street number).
   - Address does not contain at least one word (street name, 2+ letters).
   - Address does not contain a comma (`,`).
   - Address does not have at least two comma-separated parts.
   - The last part does not contain a two-letter state code (optionally followed by a zip code).

3. **Identical Addresses**
   - Source and destination addresses are the same (case-insensitive, trimmed).

4. **API/Network Error**
   - The backend cannot be reached, or returns a non-OK response.

5. **Backend Error Message**
   - Any error message returned by the backend is shown in a toast.

---

## Backend Error Conditions (FastAPI)

1. **Request Validation Error**
   - Source or destination does not match the Pydantic schema (e.g., too short, invalid characters).

2. **Geocoding Failure**
   - Address cannot be found by Nominatim after all retries.
   - Address is not matched in the geocoding result (no address part matches the display name).

3. **Database Error**
   - Failure to save the query to the database (e.g., DB connection issue).

4. **Rate Limiting**
   - Too many requests from the same client (HTTP 429).

---

## Geocoding-Specific Backend Errors
- No result from Nominatim for the address (after cleaning and retries).
- The geocoding result does not contain any part of the input address in its display name (to avoid totally irrelevant results).
- Network or HTTP error when calling Nominatim.

---

## Error Reporting
- **Frontend:** Shows a toast notification with a specific error message.
- **Backend:** Returns HTTP 400 (bad request) for geocoding/validation errors, HTTP 500 for DB errors, HTTP 429 for rate limiting.

---

**See also:**
- `src/routes/+page.svelte` for frontend validation logic
- `backend/main.py` and `backend/utils.py` for backend error handling
- E2E and unit tests in `tests/e2e/` and `tests/unit/` 