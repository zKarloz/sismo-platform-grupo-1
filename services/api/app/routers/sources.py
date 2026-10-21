"""Router de consulta pública de fuentes sísmicas."""

# ============================================================
# BLOQUE 1: Dependencias y rutas GET protegidas por DB de lectura.
# ============================================================
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.sources import list_sources
from app.schemas.source import SourceRead

router = APIRouter(prefix="/api/v1/sources", tags=["Fuentes"])


@router.get("", response_model=list[SourceRead])
def get_sources(db: Annotated[Session, Depends(get_db)]) -> list[SourceRead]:
    """Devuelve únicamente los campos públicos del catálogo de fuentes."""
    return list_sources(db)
