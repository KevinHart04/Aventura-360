import { expect, test } from "@playwright/test";

test("la web carga y el backend responde", async ({ page }) => {
  await page.goto("/");

  await expect(page.getByTestId("api-status")).toHaveText("API: ok");
});
