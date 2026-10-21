"""Lectura filtrada de coordenadas sísmicas para GeoJSON."""

# ============================================================
# BLOQUE 1: Dependencias y condiciones de filtros reutilizadas.
# ============================================================
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.data_source import DataSource
from app.models.seismic_event import SeismicEvent
from app.repositories.events import EventFilters, build_conditions
from app.schemas.geojson import EventFeature, EventProperties, FeatureCollection, PointGeometry


# ============================================================
# BLOQUE 2: Proyectar solo eventos ubicables en el mapa.
# Las coordenadas se ordenan [longitude, latitude].
# ============================================================
def list_events_geojson(
    db: Session, filters: EventFilters, *, limit: int, offset: int
) -> FeatureCollection:
    query = (
        select(SeismicEvent, DataSource.name)
        .outerjoin(DataSource, SeismicEvent.source_id == DataSource.id)
        .where(
            *build_conditions(filters),
            SeismicEvent.latitude.between(-90, 90),
            SeismicEvent.longitude.between(-180, 180),
        )
        .order_by(SeismicEvent.occurred_at.desc().nulls_last(), SeismicEvent.id.desc())
        .limit(limit)
        .offset(offset)
    )

    features = []
    for event, source_name in db.execute(query).all():
        features.append(EventFeature(
            id=event.id,
            geometry=PointGeometry(coordinates=(float(event.longitude), float(event.latitude))),
            properties=EventProperties(
                source_id=event.source_id,
                source_name=source_name,
                external_id=event.external_id,
                occurred_at=event.occurred_at,
                magnitude=float(event.magnitude) if event.magnitude is not None else None,
                depth_km=float(event.depth_km) if event.depth_km is not None else None,
                place=event.place,
            ),
        ))
    return FeatureCollection(features=features)
