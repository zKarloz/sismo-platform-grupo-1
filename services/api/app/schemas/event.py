"""Contratos HTTP de los eventos sísmicos (versión P0)."""

# ============================================================
# BLOQUE 1: Tipos públicos y serialización de fechas en UTC.
# ============================================================
from datetime import UTC, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_serializer


class EventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    source_id: UUID | None
    source_name: str | None = None
    external_id: str | None
    occurred_at: datetime | None
    latitude: float | None
    longitude: float | None
    magnitude: float | None
    magnitude_type: str | None
    depth_km: float | None
    place: str | None
    source_url: str | None
    received_at: datetime
    review_status: str

    @field_serializer("occurred_at", "received_at", when_used="json")
    def serialize_utc(self, value: datetime | None) -> str | None:
        if value is None:
            return None
        # PostgreSQL entrega timestamptz con zona. SQLite de prueba no.
        utc_value = value.replace(tzinfo=UTC) if value.tzinfo is None else value.astimezone(UTC)
        return utc_value.isoformat().replace("+00:00", "Z")


# ============================================================
# BLOQUE 2: Respuesta paginada estable para React.
# ============================================================
class EventsPage(BaseModel):
    items: list[EventRead]
    total: int
    limit: int
    offset: int
