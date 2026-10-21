"""Métricas agregadas de eventos con filtros compartidos."""

# ============================================================
# BLOQUE 1: Agregados ejecutados directamente por PostgreSQL.
# ============================================================
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.seismic_event import SeismicEvent
from app.repositories.events import EventFilters, build_conditions
from app.schemas.dashboard import DashboardSummary


# ============================================================
# BLOQUE 2: Devolver null cuando no hay datos para promediar.
# Nunca inventar actividad sísmica ni transformar null en 0.
# ============================================================
def summarize_events(db: Session, filters: EventFilters) -> DashboardSummary:
    query = select(
        func.count(SeismicEvent.id),
        func.max(SeismicEvent.occurred_at),
        func.avg(SeismicEvent.magnitude),
        func.avg(SeismicEvent.depth_km),
    ).where(*build_conditions(filters))
    total, latest, average_magnitude, average_depth = db.execute(query).one()
    return DashboardSummary(
        total_events=total,
        latest_event_at=latest,
        average_magnitude=float(average_magnitude) if average_magnitude is not None else None,
        average_depth_km=float(average_depth) if average_depth is not None else None,
    )
