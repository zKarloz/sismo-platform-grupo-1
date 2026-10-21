"""Esquemas GeoJSON estándar para el módulo de mapa sísmico."""

# ============================================================
# BLOQUE 1: Geometría y propiedades públicas, sin secretos.
# ============================================================
from datetime import UTC, datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, field_serializer


class PointGeometry(BaseModel):
    type: Literal["Point"] = "Point"
    coordinates: tuple[float, float]  # Orden GeoJSON: longitud, latitud.


class EventProperties(BaseModel):
    source_id: UUID | None
    source_name: str | None
    external_id: str | None
    occurred_at: datetime | None
    magnitude: float | None
    depth_km: float | None
    place: str | None

    @field_serializer("occurred_at", when_used="json")
    def serialize_utc(self, value: datetime | None) -> str | None:
        if value is None:
            return None
        in_utc = value.replace(tzinfo=UTC) if value.tzinfo is None else value.astimezone(UTC)
        return in_utc.isoformat().replace("+00:00", "Z")


# ============================================================
# BLOQUE 2: Colección cartográfica filtrada y paginada.
# ============================================================
class EventFeature(BaseModel):
    type: Literal["Feature"] = "Feature"
    id: UUID
    geometry: PointGeometry
    properties: EventProperties


class FeatureCollection(BaseModel):
    type: Literal["FeatureCollection"] = "FeatureCollection"
    features: list[EventFeature]
