"""Modelo de lectura de los eventos sísmicos normalizados."""

# ============================================================
# BLOQUE 1: Mapeo del esquema aplicado (UUID y numeric libre).
# Estos modelos NO crean ni alteran tablas en Supabase.
# ============================================================
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class SeismicEvent(Base):
    __tablename__ = "seismic_events"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    source_id: Mapped[UUID | None] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("data_sources.id"), nullable=True
    )
    external_id: Mapped[str | None] = mapped_column(Text)
    occurred_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    latitude: Mapped[Decimal | None] = mapped_column(Numeric)
    longitude: Mapped[Decimal | None] = mapped_column(Numeric)
    magnitude: Mapped[Decimal | None] = mapped_column(Numeric)
    magnitude_type: Mapped[str | None] = mapped_column(String)
    depth_km: Mapped[Decimal | None] = mapped_column(Numeric)
    place: Mapped[str | None] = mapped_column(Text)
    source_url: Mapped[str | None] = mapped_column(Text)
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    review_status: Mapped[str] = mapped_column(String(30), nullable=False)
