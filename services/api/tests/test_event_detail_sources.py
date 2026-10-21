"""Pruebas de detalle de eventos y fuentes, sin conexión a Supabase."""

# ============================================================
# BLOQUE 1: Preparación del SQLite aislado y dependencias.
# ============================================================
import unittest
from datetime import UTC, datetime
from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import get_db
from app.main import app
from app.models import DataSource, SeismicEvent
from app.models.base import Base


class DetailAndSourcesTests(unittest.TestCase):
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
    # BLOQUE 2: Fuentes vacías y proyección sin secretos.
    # ========================================================
    def test_sources_empty(self) -> None:
        response = self.client.get("/api/v1/sources")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_sources_hide_config_ref(self) -> None:
        source_id = uuid4()
        with self.sessions() as db:
            db.add(DataSource(
                id=source_id, name="USGS", source_type="api", status="active",
                last_sync_at=datetime(2026, 10, 21, 10, tzinfo=UTC),
                created_at=datetime(2026, 10, 21, tzinfo=UTC),
                config_ref="internal-secret-location",
            ))
            db.commit()
        response = self.client.get("/api/v1/sources")
        self.assertEqual(response.status_code, 200)
        payload = response.json()[0]
        self.assertEqual(payload["id"], str(source_id))
        self.assertEqual(payload["name"], "USGS")
        self.assertEqual(payload["last_sync_at"], "2026-10-21T10:00:00Z")
        self.assertNotIn("config_ref", payload)

    # ========================================================
    # BLOQUE 3: Detalle válido, inexistente y UUID inválido.
    # ========================================================
    def test_detail_found(self) -> None:
        source_id, event_id = uuid4(), uuid4()
        with self.sessions() as db:
            db.add(DataSource(id=source_id, name="USGS", created_at=datetime.now(UTC)))
            db.add(SeismicEvent(
                id=event_id, source_id=source_id,
                created_at=datetime.now(UTC), received_at=datetime.now(UTC),
                occurred_at=datetime(2026, 10, 20, 18, tzinfo=UTC),
                review_status="pending", external_id="test-event-001",
            ))
            db.commit()
        response = self.client.get(f"/api/v1/events/{event_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], str(event_id))
        self.assertEqual(response.json()["source_name"], "USGS")

    def test_detail_not_found(self) -> None:
        response = self.client.get(f"/api/v1/events/{uuid4()}")
        self.assertEqual(response.status_code, 404)

    def test_detail_invalid_uuid(self) -> None:
        response = self.client.get("/api/v1/events/uuid-invalido")
        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
