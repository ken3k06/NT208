import { test, expect } from "@playwright/test";

test("homepage shows project title", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "CVHT Smart Advisor" })).toBeVisible();
});
