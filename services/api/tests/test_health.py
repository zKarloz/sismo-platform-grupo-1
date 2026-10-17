"""Pruebas unitarias ligeras de los endpoints base."""

# ============================================================
# 1. IMPORTACIONES Y CLIENTE DE PRUEBAS
# ============================================================
import unittest

from fastapi.testclient import TestClient

from app.main import app


# ============================================================
# 2. PRUEBAS HTTP: RESPUESTAS Y CORS
# ============================================================
class HealthEndpointTests(unittest.TestCase):
    """La API debe responder correctamente sin PostgreSQL."""

    def setUp(self) -> None:
        self.client = TestClient(app)

    def tearDown(self) -> None:
        self.client.close()

    def test_health(self) -> None:
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_api_v1_status(self) -> None:
        response = self.client.get("/api/v1/status")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["api_version"], "v1")

    def test_cors_for_local_frontend(self) -> None:
        response = self.client.get(
            "/health", headers={"Origin": "http://localhost:5173"}
        )
        self.assertEqual(
            response.headers.get("access-control-allow-origin"),
            "http://localhost:5173",
        )


# ============================================================
# 3. EJECUCIÓN DIRECTA OPCIONAL
# ============================================================
if __name__ == "__main__":
    unittest.main()
