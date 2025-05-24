# Test info

- Name: Distance Calculator E2E >> shows error for network error during geocoding
- Location: /Users/arundhatichakraborty/FarFetchr/tests/e2e/distance-calculator.spec.ts:81:3

# Error details

```
Error: Timed out 10000ms waiting for expect(locator).toBeVisible()

Locator: getByText('Network error. Please try again later.')
Expected: visible
Received: <element(s) not found>
Call log:
  - expect.toBeVisible with timeout 10000ms
  - waiting for getByText('Network error. Please try again later.')

    at /Users/arundhatichakraborty/FarFetchr/tests/e2e/distance-calculator.spec.ts:90:76
```

# Page snapshot

```yaml
- heading "Distance Calculator" [level=1]
- paragraph: Prototype web application for calculating the distance between addresses.
- button "View Historical Queries":
  - text: View Historical Queries
  - img
- text: Source Address
- textbox "Source Address": 415 Mission St, San Francisco, CA
- button "Calculate Distance":
  - text: Calculate Distance
  - img
- text: Destination Address
- textbox "Destination Address": 1600 Amphitheatre Parkway, Mountain View, CA
- group "Unit":
  - text: Unit
  - radio "Miles"
  - text: Miles
  - radio "Kilometers"
  - text: Kilometers
  - radio "Both" [checked]
  - text: Both
- text: Distance 30.57 mi / 49.20 km
```

# Test source

```ts
   1 | import { test, expect } from '@playwright/test';
   2 |
   3 | // Adjust these addresses to ones that will work with your geocoding API
   4 | const SOURCE = '415 Mission St, San Francisco, CA';
   5 | const DEST = '1600 Amphitheatre Parkway, Mountain View, CA';
   6 |
   7 | // The expected result will depend on the geocoding and haversine calculation
   8 | // We'll just check that a result appears and is formatted
   9 |
   10 | test.describe('Distance Calculator E2E', () => {
   11 |   test('calculates distance between two addresses', async ({ page }) => {
   12 |     await page.goto('http://localhost:5173');
   13 |
   14 |     // Fill in source and destination
   15 |     await page.getByLabel('Source Address').fill(SOURCE);
   16 |     await page.getByLabel('Destination Address').fill(DEST);
   17 |
   18 |     // Select 'Both' units
   19 |     await page.getByLabel('Both').check();
   20 |
   21 |     // Click Calculate
   22 |     const button = await page.getByRole('button', { name: /calculate distance/i });
   23 |     await button.click();
   24 |
   25 |     // Wait for result to appear (result is shown in a span with id 'distance-value')
   26 |     await expect(page.getByText(/mi/)).toBeVisible({ timeout: 10000 });
   27 |     await expect(page.getByText(/km/)).toBeVisible({ timeout: 10000 });
   28 |   });
   29 |
   30 |   test('shows error for empty fields', async ({ page }) => {
   31 |     await page.goto('http://localhost:5173');
   32 |     const button = await page.getByRole('button', { name: /calculate distance/i });
   33 |     await expect(button).toBeDisabled();
   34 |   });
   35 |
   36 |   test('shows error for invalid source address', async ({ page }) => {
   37 |     await page.goto('http://localhost:5173');
   38 |     await page.getByLabel('Source Address').fill('123');
   39 |     await page.getByLabel('Destination Address').fill(DEST);
   40 |     const button = await page.getByRole('button', { name: /calculate distance/i });
   41 |     await button.click();
   42 |     await expect(page.getByText('Please enter a valid source address.')).toBeVisible();
   43 |   });
   44 |
   45 |   test('shows error for identical addresses', async ({ page }) => {
   46 |     await page.goto('http://localhost:5173');
   47 |     await page.getByLabel('Source Address').fill(SOURCE);
   48 |     await page.getByLabel('Destination Address').fill(SOURCE);
   49 |     const button = await page.getByRole('button', { name: /calculate distance/i });
   50 |     await button.click();
   51 |     await expect(page.getByText('Source and destination addresses cannot be the same.')).toBeVisible();
   52 |   });
   53 |
   54 |   test('history page shows previous queries', async ({ page }) => {
   55 |     await page.goto('http://localhost:5173');
   56 |     // Add a query to history
   57 |     await page.getByLabel('Source Address').fill(SOURCE);
   58 |     await page.getByLabel('Destination Address').fill(DEST);
   59 |     await page.getByLabel('Both').check();
   60 |     const button = await page.getByRole('button', { name: /calculate distance/i });
   61 |     await button.click();
   62 |     await expect(page.getByText(/mi/)).toBeVisible({ timeout: 10000 });
   63 |     // Go to history page
   64 |     await page.getByRole('button', { name: /view historical queries/i }).click();
   65 |     // Check that the history table contains the addresses (use .first() to avoid strict mode violation)
   66 |     await expect(page.getByText(SOURCE).first()).toBeVisible();
   67 |     await expect(page.getByText(DEST).first()).toBeVisible();
   68 |   });
   69 |
   70 |   test('shows error for unfindable address (geocoding failure)', async ({ page }) => {
   71 |     // NOTE: If this test fails, manually verify the error message in the UI and adjust the test or frontend as needed.
   72 |     await page.goto('http://localhost:5173');
   73 |     await page.getByLabel('Source Address').fill('ThisAddressDoesNotExist1234567890');
   74 |     await page.getByLabel('Destination Address').fill(DEST);
   75 |     await page.getByLabel('Both').check();
   76 |     const button = await page.getByRole('button', { name: /calculate distance/i });
   77 |     await button.click();
   78 |     await expect(page.getByText('Please enter a valid source address.')).toBeVisible({ timeout: 10000 });
   79 |   });
   80 |
   81 |   test('shows error for network error during geocoding', async ({ page }) => {
   82 |     // NOTE: If this test fails, manually verify the error message in the UI and adjust the test or frontend as needed.
   83 |     await page.route('**/nominatim.openstreetmap.org/**', route => route.abort());
   84 |     await page.goto('http://localhost:5173');
   85 |     await page.getByLabel('Source Address').fill(SOURCE);
   86 |     await page.getByLabel('Destination Address').fill(DEST);
   87 |     await page.getByLabel('Both').check();
   88 |     const button = await page.getByRole('button', { name: /calculate distance/i });
   89 |     await button.click();
>  90 |     await expect(page.getByText('Network error. Please try again later.')).toBeVisible({ timeout: 10000 });
      |                                                                            ^ Error: Timed out 10000ms waiting for expect(locator).toBeVisible()
   91 |   });
   92 |
   93 |   test('has accessible labels and roles', async ({ page }) => {
   94 |     await page.goto('http://localhost:5173');
   95 |     // Check for accessible labels
   96 |     await expect(page.getByLabel('Source Address')).toBeVisible();
   97 |     await expect(page.getByLabel('Destination Address')).toBeVisible();
   98 |     await expect(page.getByLabel('Miles')).toBeVisible();
   99 |     await expect(page.getByLabel('Kilometers')).toBeVisible();
  100 |     await expect(page.getByLabel('Both')).toBeVisible();
  101 |     // Check for accessible button
  102 |     await expect(page.getByRole('button', { name: /calculate distance/i })).toBeVisible();
  103 |     await expect(page.getByRole('button', { name: /view historical queries/i })).toBeVisible();
  104 |   });
  105 |
  106 |   test('works on mobile viewport', async ({ page }) => {
  107 |     await page.setViewportSize({ width: 375, height: 700 }); // iPhone X size
  108 |     await page.goto('http://localhost:5173');
  109 |     await page.getByLabel('Source Address').fill(SOURCE);
  110 |     await page.getByLabel('Destination Address').fill(DEST);
  111 |     await page.getByLabel('Both').check();
  112 |     const button = await page.getByRole('button', { name: /calculate distance/i });
  113 |     await button.click();
  114 |     await expect(page.getByText(/mi/)).toBeVisible({ timeout: 10000 });
  115 |     await expect(page.getByText(/km/)).toBeVisible({ timeout: 10000 });
  116 |     // Check that the layout is still usable (e.g., form is visible)
  117 |     await expect(page.getByLabel('Source Address')).toBeVisible();
  118 |     await expect(page.getByLabel('Destination Address')).toBeVisible();
  119 |   });
  120 | }); 
```