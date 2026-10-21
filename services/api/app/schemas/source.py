"""Respuesta pública mínima para fuentes de eventos sísmicos."""

# ============================================================
# BLOQUE 1: Esquema de lectura; excluir configuraciones privadas.
# ============================================================
from datetime import UTC, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_serializer


class SourceRead(BaseModel):
    """Campos públicos permitidos en GET /api/v1/sources."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str | None
    source_type: str | None
    status: str | None
    last_sync_at: datetime | None

    # ========================================================
    # BLOQUE 2: Fechas emitidas en UTC para el frontend.
    # ========================================================
    @field_serializer("last_sync_at", when_used="json")
    def serialize_utc(self, value: datetime | None) -> str | None:
        if value is None:
            return None
        utc_value = value.replace(tzinfo=UTC) if value.tzinfo is None else value.astimezone(UTC)
        return utc_value.isoformat().replace("+00:00", "Z")
