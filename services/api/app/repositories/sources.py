"""Consultas de solo lectura sobre fuentes disponibles."""

# ============================================================
# BLOQUE 1: Selección tipada, sin exponer config_ref.
# ============================================================
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.data_source import DataSource
from app.schemas.source import SourceRead


def list_sources(db: Session) -> list[SourceRead]:
    """Lista fuentes de forma determinista para filtros del frontend."""
    statement = select(DataSource).order_by(DataSource.name.asc().nulls_last(), DataSource.id)
    return [SourceRead.model_validate(source) for source in db.scalars(statement).all()]
