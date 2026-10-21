"""Contrato REST del resumen estadístico del dashboard."""

# ============================================================
# BLOQUE 1: Métricas agregadas y fechas UTC explícitas.
# ============================================================
from datetime import UTC, datetime

from pydantic import BaseModel, field_serializer


class DashboardSummary(BaseModel):
    total_events: int
    latest_event_at: datetime | None
    average_magnitude: float | None
    average_depth_km: float | None

    @field_serializer("latest_event_at", when_used="json")
    def serialize_utc(self, value: datetime | None) -> str | None:
        if value is None:
            return None
        in_utc = value.replace(tzinfo=UTC) if value.tzinfo is None else value.astimezone(UTC)
        return in_utc.isoformat().replace("+00:00", "Z")
