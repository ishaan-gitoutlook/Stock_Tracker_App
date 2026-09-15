/**
 * 📘 Lesson 2.2 — Locator Strategies
 *
 * This lesson teaches you all the ways to find elements on a page.
 * We'll use the Playwright TodoMVC demo app — a real, interactive app.
 *
 * WHY THIS MATTERS FOR MCP:
 *   When an AI uses MCP, it sees the accessibility tree, which contains
 *   roles and names — exactly what getByRole() and getByLabel() use.
 *   Writing tests this way trains your brain for AI-driven automation.
 *
 * Run:
 *   npx playwright test tests/e2e/02-locators.spec.ts --headed
 */
import { test, expect } from '@playwright/test';

const TODO_URL = 'https://demo.playwright.dev/todomvc/#/';

// ─── 1. getByPlaceholder() — Find by placeholder text ───────────
// Best for: Input fields with placeholder text
// AI equivalent: The AI sees "textbox 'What needs to be done?'"

test('getByPlaceholder: Add a todo item', async ({ page }) => {
  await page.goto(TODO_URL);

  // Find the input by its placeholder text
  const input = page.getByPlaceholder('What needs to be done?');

  // Type a todo and press Enter
  await input.fill('Learn Playwright locators');
  await input.press('Enter');

  // Verify it appeared
  await expect(page.getByText('Learn Playwright locators')).toBeVisible();
});


// ─── 2. getByRole() — Find by accessibility role ────────────────
// Best for: Buttons, links, checkboxes, headings — any standard UI element
// AI equivalent: EXACTLY what MCP sends to the AI!
//
// ⚠️ LESSON: Sometimes the accessible name isn't what you expect!
//    TodoMVC's checkboxes don't use the todo text as their name.
//    This teaches an important debugging skill for MCP work too.

test('getByRole: Check and uncheck a todo', async ({ page }) => {
  await page.goto(TODO_URL);

  // Add a todo first
  await page.getByPlaceholder('What needs to be done?').fill('Master getByRole');
  await page.getByPlaceholder('What needs to be done?').press('Enter');

  // APPROACH: Find the todo item, then find the checkbox WITHIN it
  // This is "chaining" — narrow down your search area first
  const todoItem = page.getByText('Master getByRole');
  const checkbox = todoItem.locator('..').getByRole('checkbox');

  // Check it
  await checkbox.check();
  await expect(checkbox).toBeChecked();

  // Uncheck it
  await checkbox.uncheck();
  await expect(checkbox).not.toBeChecked();
});


// ─── 3. getByText() — Find by visible text content ──────────────
// Best for: Labels, paragraphs, error messages
// Caution: Can match multiple elements — use exact: true when needed

test('getByText: Verify todo text appears', async ({ page }) => {
  await page.goto(TODO_URL);

  // Add multiple todos
  const input = page.getByPlaceholder('What needs to be done?');
  await input.fill('Buy groceries');
  await input.press('Enter');
  await input.fill('Walk the dog');
  await input.press('Enter');

  // Find by exact text
  await expect(page.getByText('Buy groceries')).toBeVisible();
  await expect(page.getByText('Walk the dog')).toBeVisible();

  // Partial match — finds any text CONTAINING "dog"
  await expect(page.getByText('dog')).toBeVisible();

  // Exact match — won't find partial text
  await expect(page.getByText('Buy groceries', { exact: true })).toBeVisible();
});


// ─── 4. getByRole() with links — Navigation elements ────────────
// Links are one of the most common roles in web apps

test('getByRole link: Filter todos', async ({ page }) => {
  await page.goto(TODO_URL);

  // Add and complete a todo
  const input = page.getByPlaceholder('What needs to be done?');
  await input.fill('Completed task');
  await input.press('Enter');
  await input.fill('Active task');
  await input.press('Enter');

  // Complete the first one — use chaining (same pattern as Lesson 2)
  await page.getByText('Completed task').locator('..').getByRole('checkbox').check();

  // Click the "Active" filter link
  await page.getByRole('link', { name: 'Active' }).click();

  // Only active task should be visible
  await expect(page.getByText('Active task')).toBeVisible();
  await expect(page.getByText('Completed task')).not.toBeVisible();

  // Click "Completed" filter
  await page.getByRole('link', { name: 'Completed' }).click();

  // Now only completed task should be visible
  await expect(page.getByText('Completed task')).toBeVisible();
  await expect(page.getByText('Active task')).not.toBeVisible();
});


// ─── 5. Chaining locators — Complex element finding ─────────────
// Sometimes you need to narrow down: "the button INSIDE the header"

test('Chaining: Find elements within a section', async ({ page }) => {
  await page.goto(TODO_URL);

  // Add a todo
  const input = page.getByPlaceholder('What needs to be done?');
  await input.fill('Chaining example');
  await input.press('Enter');

  // Chain locators: find the todo list, then find items within it
  // Using .locator('.todo-list') to target the specific list (not nav lists)
  const todoList = page.locator('.todo-list');
  const todoItems = todoList.getByRole('listitem');

  // Verify count
  await expect(todoItems).toHaveCount(1);

  // Add another
  await input.fill('Second item');
  await input.press('Enter');
  await expect(todoItems).toHaveCount(2);
});


// ─── 6. BONUS: Locator assertions (what to check) ───────────────
// A reference of common assertions you'll use

test('Assertion reference: Common checks', async ({ page }) => {
  await page.goto(TODO_URL);

  const input = page.getByPlaceholder('What needs to be done?');
  await input.fill('Assertion demo');
  await input.press('Enter');

  const todoText = page.getByText('Assertion demo');
  // Use chaining to find the checkbox (same lesson as test 2!)
  const checkbox = todoText.locator('..').getByRole('checkbox');

  // Visibility
  await expect(todoText).toBeVisible();

  // Enabled/Disabled
  await expect(checkbox).toBeEnabled();

  // Checked/Unchecked
  await expect(checkbox).not.toBeChecked();
  await checkbox.check();
  await expect(checkbox).toBeChecked();

  // Text content
  await expect(todoText).toHaveText('Assertion demo');
  await expect(todoText).toContainText('demo');

  // Count (for multiple elements)
  await expect(page.locator('.todo-list').getByRole('listitem')).toHaveCount(1);
});
