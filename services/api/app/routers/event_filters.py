"""Validaciones de filtros compartidas entre eventos, mapa y dashboard."""

# ============================================================
# BLOQUE 1: Tipos y dependencias del contrato REST P0.
# ============================================================
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from fastapi import HTTPException

from app.repositories.events import EventFilters


# ============================================================
# BLOQUE 2: Valida intervalos y fechas con zona horaria.
# - start_at es inclusivo; end_at es exclusivo.
# - Conservar el mismo comportamiento para todos los endpoints.
# ============================================================
def parse_event_filters(
    start_at: datetime | None,
    end_at: datetime | None,
    min_magnitude: Decimal | None,
    max_magnitude: Decimal | None,
    source_id: UUID | None,
) -> EventFilters:
    for name, value in (("start_at", start_at), ("end_at", end_at)):
        if value is not None and (value.tzinfo is None or value.utcoffset() is None):
            raise HTTPException(status_code=422, detail=f"{name} debe incluir zona horaria")

    if start_at is not None and end_at is not None and end_at <= start_at:
        raise HTTPException(status_code=422, detail="end_at debe ser posterior a start_at")
    if (
        min_magnitude is not None
        and max_magnitude is not None
        and max_magnitude < min_magnitude
    ):
        raise HTTPException(status_code=422, detail="max_magnitude debe ser >= min_magnitude")

    return EventFilters(
        start_at=start_at,
        end_at=end_at,
        min_magnitude=min_magnitude,
        max_magnitude=max_magnitude,
        source_id=source_id,
    )
