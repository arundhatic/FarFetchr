import { test, expect } from '@playwright/test';

// Adjust these addresses to ones that will work with your geocoding API
const SOURCE = '415 Mission St, San Francisco, CA';
const DEST = '1600 Amphitheatre Parkway, Mountain View, CA';

// The expected result will depend on the geocoding and haversine calculation
// We'll just check that a result appears and is formatted

test.describe('Distance Calculator E2E', () => {
  test('calculates distance between two addresses', async ({ page }) => {
    await page.goto('/');

    // Fill in source and destination
    await page.getByLabel('Source Address').fill(SOURCE);
    await page.getByLabel('Destination Address').fill(DEST);

    // Select 'Both' units
    await page.getByLabel('Both').check();

    // Click Calculate
    const button = await page.getByRole('button', { name: /calculate distance/i });
    await button.click();

    // Wait for result to appear (result is shown in a span with id 'distance-value')
    await expect(page.getByText(/mi/)).toBeVisible({ timeout: 10000 });
    await expect(page.getByText(/km/)).toBeVisible({ timeout: 10000 });
  });

  test('shows error for empty fields', async ({ page }) => {
    await page.goto('/');
    const button = await page.getByRole('button', { name: /calculate distance/i });
    await expect(button).toBeDisabled();
  });

  test('shows error for invalid source address', async ({ page }) => {
    await page.goto('/');
    await page.getByLabel('Source Address').fill('123');
    await page.getByLabel('Destination Address').fill(DEST);
    const button = await page.getByRole('button', { name: /calculate distance/i });
    await button.click();
    await expect(page.getByText('Please enter a valid source address.')).toBeVisible();
  });

  test('shows error for identical addresses', async ({ page }) => {
    await page.goto('/');
    await page.getByLabel('Source Address').fill(SOURCE);
    await page.getByLabel('Destination Address').fill(SOURCE);
    const button = await page.getByRole('button', { name: /calculate distance/i });
    await button.click();
    await expect(page.getByText('Source and destination addresses cannot be the same.')).toBeVisible();
  });

  test('history page shows previous queries', async ({ page }) => {
    await page.goto('/');
    // Add a query to history
    await page.getByLabel('Source Address').fill(SOURCE);
    await page.getByLabel('Destination Address').fill(DEST);
    await page.getByLabel('Both').check();
    const button = await page.getByRole('button', { name: /calculate distance/i });
    await button.click();
    await expect(page.getByText(/mi/)).toBeVisible({ timeout: 10000 });
    // Go to history page
    await page.getByRole('button', { name: /view historical queries/i }).click();
    // Check that the history table contains the addresses (use .first() to avoid strict mode violation)
    await expect(page.getByText(SOURCE).first()).toBeVisible();
    await expect(page.getByText(DEST).first()).toBeVisible();
  });

  test('shows error for unfindable address (geocoding failure)', async ({ page }) => {
    // NOTE: If this test fails, manually verify the error message in the UI and adjust the test or frontend as needed.
    await page.goto('/');
    await page.getByLabel('Source Address').fill('ThisAddressDoesNotExist1234567890');
    await page.getByLabel('Destination Address').fill(DEST);
    await page.getByLabel('Both').check();
    const button = await page.getByRole('button', { name: /calculate distance/i });
    await button.click();
    await expect(page.getByText('Please enter a valid source address.')).toBeVisible({ timeout: 10000 });
  });

  test('has accessible labels and roles', async ({ page }) => {
    await page.goto('/');
    // Check for accessible labels
    await expect(page.getByLabel('Source Address')).toBeVisible();
    await expect(page.getByLabel('Destination Address')).toBeVisible();
    await expect(page.getByLabel('Miles')).toBeVisible();
    await expect(page.getByLabel('Kilometers')).toBeVisible();
    await expect(page.getByLabel('Both')).toBeVisible();
    // Check for accessible button
    await expect(page.getByRole('button', { name: /calculate distance/i })).toBeVisible();
    await expect(page.getByRole('button', { name: /view historical queries/i })).toBeVisible();
  });

  test('works on mobile viewport', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 700 }); // iPhone X size
    await page.goto('/');
    await page.getByLabel('Source Address').fill(SOURCE);
    await page.getByLabel('Destination Address').fill(DEST);
    await page.getByLabel('Both').check();
    const button = await page.getByRole('button', { name: /calculate distance/i });
    await button.click();
    await expect(page.getByText(/mi/)).toBeVisible({ timeout: 10000 });
    await expect(page.getByText(/km/)).toBeVisible({ timeout: 10000 });
    // Check that the layout is still usable (e.g., form is visible)
    await expect(page.getByLabel('Source Address')).toBeVisible();
    await expect(page.getByLabel('Destination Address')).toBeVisible();
  });
}); 