"""Consulta de eventos sísmicos y representación GeoJSON (fases 3/4)."""

# ============================================================
# BLOQUE 1: Dependencias HTTP, filtros y servicios de lectura.
# ============================================================
from datetime import datetime
from decimal import Decimal
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.events import find_event, list_events
from app.repositories.geojson import list_events_geojson
from app.routers.event_filters import parse_event_filters
from app.schemas.event import EventRead, EventsPage
from app.schemas.geojson import FeatureCollection

router = APIRouter(prefix="/api/v1/events", tags=["Eventos"])


# ============================================================
# BLOQUE 2: GET /events (paginación de 1 a 100 elementos).
# ============================================================
@router.get("", response_model=EventsPage)
def get_events(
    db: Annotated[Session, Depends(get_db)],
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
    start_at: datetime | None = None,
    end_at: datetime | None = None,
    min_magnitude: Decimal | None = None,
    max_magnitude: Decimal | None = None,
    source_id: UUID | None = None,
) -> EventsPage:
    filters = parse_event_filters(start_at, end_at, min_magnitude, max_magnitude, source_id)
    return list_events(db, filters, limit=limit, offset=offset)


# ============================================================
# BLOQUE 3: GET /events/geojson (ruta fija ANTES del UUID).
# El mapa solo muestra registros con coordenadas válidas.
# ============================================================
@router.get("/geojson", response_model=FeatureCollection, tags=["Mapa"])
def get_events_geojson(
    db: Annotated[Session, Depends(get_db)],
    limit: Annotated[int, Query(ge=1, le=500)] = 200,
    offset: Annotated[int, Query(ge=0)] = 0,
    start_at: datetime | None = None,
    end_at: datetime | None = None,
    min_magnitude: Decimal | None = None,
    max_magnitude: Decimal | None = None,
    source_id: UUID | None = None,
) -> FeatureCollection:
    filters = parse_event_filters(start_at, end_at, min_magnitude, max_magnitude, source_id)
    return list_events_geojson(db, filters, limit=limit, offset=offset)


# ============================================================
# BLOQUE 4: GET /events/{UUID} (200, 404 y 422).
# ============================================================
@router.get("/{event_id}", response_model=EventRead)
def get_event_detail(
    event_id: UUID, db: Annotated[Session, Depends(get_db)]
) -> EventRead:
    event = find_event(db, event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Evento sísmico no encontrado")
    return event
