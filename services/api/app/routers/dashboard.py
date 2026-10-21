"""Endpoint de resumen ejecutivo sobre eventos sísmicos observados."""

# ============================================================
# BLOQUE 1: Parámetros equivalentes a GET /events.
# ============================================================
from datetime import datetime
from decimal import Decimal
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.dashboard import summarize_events
from app.routers.event_filters import parse_event_filters
from app.schemas.dashboard import DashboardSummary

router = APIRouter(prefix="/api/v1/dashboard", tags=["Dashboard"])


# ============================================================
# BLOQUE 2: GET /dashboard/summary con filtros coherentes.
# ============================================================
@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary(
    db: Annotated[Session, Depends(get_db)],
    start_at: datetime | None = None,
    end_at: datetime | None = None,
    min_magnitude: Decimal | None = None,
    max_magnitude: Decimal | None = None,
    source_id: UUID | None = None,
) -> DashboardSummary:
    filters = parse_event_filters(start_at, end_at, min_magnitude, max_magnitude, source_id)
    return summarize_events(db, filters)
