import { useEffect, useState } from "react";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000/api";

type Status = "loading" | "ok" | "error";

export default function App() {
  const [status, setStatus] = useState<Status>("loading");

  useEffect(() => {
    fetch(`${API_URL}/health/`)
      .then((res) => {
        setStatus(res.ok ? "ok" : "error");
      })
      .catch(() => {
        setStatus("error");
      });
  }, []);

  return (
    <main>
      <h1>Ecommerce</h1>
      <p data-testid="api-status">API: {status}</p>
    </main>
  );
}
