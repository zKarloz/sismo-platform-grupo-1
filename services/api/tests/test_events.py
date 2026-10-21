"""Pruebas API P0 con SQLite aislado: sin acceso a Supabase."""

# ============================================================
# BLOQUE 1: Fixtures en memoria y sustitución de get_db.
# ============================================================
import unittest
from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import get_db
from app.main import app
from app.models import DataSource, SeismicEvent
from app.models.base import Base


class EventsEndpointTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = create_engine(
            "sqlite+pysqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        Base.metadata.create_all(self.engine)
        self.sessions = sessionmaker(bind=self.engine)

        def override_db():
            with self.sessions() as db:
                yield db

        app.dependency_overrides[get_db] = override_db
        self.client = TestClient(app)

    def tearDown(self) -> None:
        self.client.close()
        app.dependency_overrides.clear()
        self.engine.dispose()

    # ========================================================
    # BLOQUE 2: Respuestas vacías, filtros y errores 422.
    # ========================================================
    def test_empty_page(self) -> None:
        response = self.client.get("/api/v1/events")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"items": [], "total": 0, "limit": 20, "offset": 0},
        )

    def test_invalid_limit(self) -> None:
        self.assertEqual(self.client.get("/api/v1/events?limit=101").status_code, 422)

    def test_naive_datetime_rejected(self) -> None:
        self.assertEqual(
            self.client.get("/api/v1/events?start_at=2026-10-21T00:00:00").status_code,
            422,
        )

    def test_reversed_dates_rejected(self) -> None:
        response = self.client.get(
            "/api/v1/events?start_at=2026-10-20T00:00:00Z"
            "&end_at=2026-10-19T00:00:00Z"
        )
        self.assertEqual(response.status_code, 422)

    # ========================================================
    # BLOQUE 3: Verificar paginación, filtros y procedencia.
    # ========================================================
    def test_filter_and_pagination(self) -> None:
        source_id = uuid4()
        with self.sessions() as db:
            db.add(
                DataSource(
                    id=source_id,
                    name="USGS",
                    created_at=datetime(2026, 10, 21, tzinfo=UTC),
                )
            )
            for value in [Decimal("3.2"), Decimal("5.1")]:
                db.add(
                    SeismicEvent(
                        id=uuid4(),
                        source_id=source_id,
                        created_at=datetime(2026, 10, 21, tzinfo=UTC),
                        received_at=datetime(2026, 10, 21, tzinfo=UTC),
                        occurred_at=datetime(2026, 10, 20, tzinfo=UTC),
                        magnitude=value,
                        review_status="pending",
                    )
                )
            db.commit()

        response = self.client.get("/api/v1/events?min_magnitude=5&limit=1")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total"], 1)
        self.assertEqual(len(data["items"]), 1)
        self.assertEqual(data["items"][0]["source_name"], "USGS")
        self.assertEqual(data["items"][0]["magnitude"], 5.1)
        self.assertTrue(data["items"][0]["occurred_at"].endswith("Z"))


# ============================================================
# BLOQUE 4: Permitir ejecutar el archivo individualmente.
# ============================================================
if __name__ == "__main__":
    unittest.main()
