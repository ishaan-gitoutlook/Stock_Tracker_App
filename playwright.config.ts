import { defineConfig, devices } from '@playwright/test';

/**
 * Playwright Configuration for Stock Tracker App
 * 
 * 📘 Lesson 1.2: This config tells Playwright:
 *   - WHERE to find tests (tests/e2e/)
 *   - WHICH browser to use (Chromium)
 *   - WHAT base URL your app runs on (localhost:8501 for Streamlit)
 */
export default defineConfig({
  // Where to find test files
  testDir: './tests/e2e',

  // Run tests one at a time (easier for learning)
  fullyParallel: false,

  // Fail the build on CI if you accidentally left test.only in the source code
  forbidOnly: !!process.env.CI,

  // Retry failed tests once (helpful for flaky network calls)
  retries: 1,

  // Reporter — shows results in terminal + generates HTML report
  reporter: [
    ['list'],           // Live progress in terminal
    ['html', { open: 'never' }]  // HTML report saved to playwright-report/
  ],

  // Shared settings for all tests
  use: {
    // Your Stock Tracker runs on this URL (Streamlit default port)
    baseURL: 'http://localhost:8501',

    // Capture screenshot on failure (great for debugging)
    screenshot: 'only-on-failure',

    // Record video on failure
    video: 'retain-on-failure',

    // Capture trace on failure (step-by-step replay — very powerful!)
    trace: 'retain-on-failure',
  },

  // Browser to test against
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    // Uncomment later to test on more browsers:
    // {
    //   name: 'firefox',
    //   use: { ...devices['Desktop Firefox'] },
    // },
    // {
    //   name: 'webkit',
    //   use: { ...devices['Desktop Safari'] },
    // },
  ],
});
