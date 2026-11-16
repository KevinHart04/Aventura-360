import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e",
  use: { baseURL: "http://localhost:5173" },
  webServer: [
    {
      command: "uv run python manage.py runserver 8000",
      cwd: "../backend",
      url: "http://localhost:8000/api/health/",
      reuseExistingServer: !process.env.CI,
    },
    {
      command: "npm run dev -- --port 5173",
      url: "http://localhost:5173",
      reuseExistingServer: !process.env.CI,
    },
  ],
});
