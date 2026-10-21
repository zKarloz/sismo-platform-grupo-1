"""Pruebas aisladas de dashboard y GeoJSON, sin acceso a Supabase."""

# ============================================================
# BLOQUE 1: Base temporal, fixtures y conexión de pruebas.
# ============================================================
import unittest
from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID, uuid4

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import get_db
from app.main import app
from app.models import DataSource, SeismicEvent
from app.models.base import Base


class DashboardGeojsonTests(unittest.TestCase):
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

    def add_sample_events(self) -> tuple[UUID, UUID]:
        source_id, second_id = uuid4(), uuid4()
        with self.sessions() as db:
            db.add_all([
                DataSource(id=source_id, name="USGS", created_at=datetime.now(UTC)),
                DataSource(id=second_id, name="IGP", created_at=datetime.now(UTC)),
            ])
            db.add_all([
                SeismicEvent(
                    id=uuid4(), source_id=source_id,
                    created_at=datetime.now(UTC), received_at=datetime.now(UTC),
                    occurred_at=datetime(2026, 10, 20, 12, tzinfo=UTC),
                    magnitude=Decimal("4.0"), depth_km=Decimal("15"),
                    latitude=Decimal("-12.050000"), longitude=Decimal("-77.010000"),
                    review_status="pending", external_id="usgs-001", place="Lima",
                ),
                SeismicEvent(
                    id=uuid4(), source_id=source_id,
                    created_at=datetime.now(UTC), received_at=datetime.now(UTC),
                    occurred_at=datetime(2026, 10, 21, 12, tzinfo=UTC),
                    magnitude=Decimal("6.0"), depth_km=Decimal("25"),
                    latitude=None, longitude=None,
                    review_status="pending", external_id="usgs-002",
                ),
                SeismicEvent(
                    id=uuid4(), source_id=second_id,
                    created_at=datetime.now(UTC), received_at=datetime.now(UTC),
                    occurred_at=datetime(2026, 10, 22, 12, tzinfo=UTC),
                    magnitude=None, depth_km=None,
                    latitude=Decimal("-10"), longitude=Decimal("-76"),
                    review_status="pending", external_id="igp-001",
                ),
            ])
            db.commit()
        return source_id, second_id

    # ========================================================
    # BLOQUE 2: Dashboard vacío, agregados y filtros.
    # ========================================================
    def test_empty_dashboard(self) -> None:
        response = self.client.get("/api/v1/dashboard/summary")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "total_events": 0, "latest_event_at": None,
            "average_magnitude": None, "average_depth_km": None,
        })

    def test_dashboard_statistics(self) -> None:
        self.add_sample_events()
        response = self.client.get("/api/v1/dashboard/summary")
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result["total_events"], 3)
        self.assertEqual(result["average_magnitude"], 5.0)
        self.assertEqual(result["average_depth_km"], 20.0)
        self.assertEqual(result["latest_event_at"], "2026-10-22T12:00:00Z")

    def test_dashboard_matches_filtered_events(self) -> None:
        source_id, _ = self.add_sample_events()
        params = {"source_id": str(source_id), "min_magnitude": "5"}
        summary = self.client.get("/api/v1/dashboard/summary", params=params).json()
        events = self.client.get("/api/v1/events", params=params).json()
        self.assertEqual(summary["total_events"], events["total"])
        self.assertEqual(summary["average_magnitude"], 6.0)

    def test_dashboard_rejects_invalid_interval(self) -> None:
        response = self.client.get("/api/v1/dashboard/summary?start_at=2026-10-21T00:00:00")
        self.assertEqual(response.status_code, 422)

    # ========================================================
    # BLOQUE 3: GeoJSON, coordenadas y paginación.
    # ========================================================
    def test_empty_geojson(self) -> None:
        response = self.client.get("/api/v1/events/geojson")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"type": "FeatureCollection", "features": []})

    def test_geojson_points_and_skip_missing(self) -> None:
        self.add_sample_events()
        response = self.client.get("/api/v1/events/geojson")
        self.assertEqual(response.status_code, 200)
        features = response.json()["features"]
        self.assertEqual(len(features), 2)
        by_external_id = {item["properties"]["external_id"]: item for item in features}
        usgs = by_external_id["usgs-001"]
        self.assertEqual(usgs["geometry"]["type"], "Point")
        self.assertEqual(usgs["geometry"]["coordinates"], [-77.01, -12.05])
        self.assertEqual(usgs["properties"]["source_name"], "USGS")
        self.assertEqual(usgs["properties"]["occurred_at"], "2026-10-20T12:00:00Z")
        self.assertNotIn("usgs-002", by_external_id)

    def test_geojson_filter_magnitude(self) -> None:
        self.add_sample_events()
        response = self.client.get("/api/v1/events/geojson?min_magnitude=5")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["features"], [])

    def test_geojson_pagination(self) -> None:
        self.add_sample_events()
        first = self.client.get("/api/v1/events/geojson?limit=1&offset=0").json()
        next_page = self.client.get("/api/v1/events/geojson?limit=1&offset=1").json()
        self.assertEqual(len(first["features"]), 1)
        self.assertEqual(len(next_page["features"]), 1)
        self.assertNotEqual(first["features"][0]["id"], next_page["features"][0]["id"])

    def test_geojson_limit_rejected(self) -> None:
        self.assertEqual(self.client.get("/api/v1/events/geojson?limit=501").status_code, 422)

    def test_geojson_fixed_route_precedes_uuid(self) -> None:
        self.assertEqual(self.client.get("/api/v1/events/geojson").status_code, 200)

    def test_geojson_rejects_naive_time(self) -> None:
        self.assertEqual(
            self.client.get("/api/v1/events/geojson?end_at=2026-10-21T00:00:00").status_code,
            422,
        )


if __name__ == "__main__":
    unittest.main()
