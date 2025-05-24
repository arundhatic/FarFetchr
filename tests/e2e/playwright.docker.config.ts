import { defineConfig } from '@playwright/test';

export default defineConfig({
  use: {
    baseURL: 'http://localhost:4173',
    // Add other Playwright options here if needed
  },
  // You can add more config (testDir, retries, etc.) as needed
}); 