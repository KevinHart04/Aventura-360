import { render, screen } from "@testing-library/react";
import { afterEach, expect, test, vi } from "vitest";

import App from "./App";

afterEach(() => {
  vi.unstubAllGlobals();
});

test("muestra API: ok cuando el backend responde", async () => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: true }));

  render(<App />);

  expect(await screen.findByText("API: ok")).toBeInTheDocument();
});

test("muestra API: error cuando el backend falla", async () => {
  vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("network")));

  render(<App />);

  expect(await screen.findByText("API: error")).toBeInTheDocument();
});
