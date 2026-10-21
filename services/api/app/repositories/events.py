"""Consultas SQLAlchemy de solo lectura, con filtros reutilizables."""

# ============================================================
# BLOQUE 1: Filtros tipados y validados para el API P0.
# ============================================================
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.data_source import DataSource
from app.models.seismic_event import SeismicEvent
from app.schemas.event import EventRead, EventsPage


@dataclass(frozen=True)
class EventFilters:
    start_at: datetime | None = None
    end_at: datetime | None = None
    min_magnitude: Decimal | None = None
    max_magnitude: Decimal | None = None
    source_id: UUID | None = None


def build_conditions(filters: EventFilters) -> list:
    conditions = []
    if filters.start_at is not None:
        conditions.append(SeismicEvent.occurred_at >= filters.start_at)
    if filters.end_at is not None:
        conditions.append(SeismicEvent.occurred_at < filters.end_at)
    if filters.min_magnitude is not None:
        conditions.append(SeismicEvent.magnitude >= filters.min_magnitude)
    if filters.max_magnitude is not None:
        conditions.append(SeismicEvent.magnitude <= filters.max_magnitude)
    if filters.source_id is not None:
        conditions.append(SeismicEvent.source_id == filters.source_id)
    return conditions


# ============================================================
# BLOQUE 2: Total y página. JOIN obtiene el nombre sin N+1.
# Orden determinista en PostgreSQL: fecha e ID descendentes.
# ============================================================
def list_events(db: Session, filters: EventFilters, limit: int, offset: int) -> EventsPage:
    conditions = build_conditions(filters)
    total = db.scalar(select(func.count()).select_from(SeismicEvent).where(*conditions)) or 0

    statement = (
        select(SeismicEvent, DataSource.name)
        .outerjoin(DataSource, SeismicEvent.source_id == DataSource.id)
        .where(*conditions)
        .order_by(SeismicEvent.occurred_at.desc().nulls_last(), SeismicEvent.id.desc())
        .limit(limit)
        .offset(offset)
    )
    items = [
        EventRead.model_validate(event).model_copy(update={"source_name": source_name})
        for event, source_name in db.execute(statement).all()
    ]
    return EventsPage(items=items, total=total, limit=limit, offset=offset)


# ============================================================
# BLOQUE 3: Detalle de evento por UUID, con nombre de fuente.
# ============================================================
def find_event(db: Session, event_id: UUID) -> EventRead | None:
    statement = (
        select(SeismicEvent, DataSource.name)
        .outerjoin(DataSource, SeismicEvent.source_id == DataSource.id)
        .where(SeismicEvent.id == event_id)
    )
    row = db.execute(statement).one_or_none()
    if row is None:
        return None
    event, source_name = row
    return EventRead.model_validate(event).model_copy(update={"source_name": source_name})
