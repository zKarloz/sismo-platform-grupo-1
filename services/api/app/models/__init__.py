"""Importaciones explícitas para registrar los modelos en Base.metadata."""

# ============================================================
# BLOQUE 1: Modelos usados en consultas de lectura.
# ============================================================
from app.models.data_source import DataSource
from app.models.seismic_event import SeismicEvent

__all__ = ["DataSource", "SeismicEvent"]
