"""Sesiones de lectura PostgreSQL para los endpoints P0."""

# ============================================================
# BLOQUE 1: Dependencias y configuración de conexión.
# La importación de este módulo NO abre una conexión.
# ============================================================
from collections.abc import Generator
from functools import lru_cache

from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings


# ============================================================
# BLOQUE 2: Motor bajo demanda, con conexiones TLS.
# Utilizar en DATABASE_URL una cuenta PostgreSQL de SOLO LECTURA.
# ============================================================
@lru_cache(maxsize=1)
def get_engine() -> Engine:
    if not settings.database_url:
        raise RuntimeError("DATABASE_URL no configurada")

    raw_url = settings.database_url
    if raw_url.startswith("postgresql+psycopg://"):
        url = raw_url
    elif raw_url.startswith("postgresql://"):
        url = raw_url.replace("postgresql://", "postgresql+psycopg://", 1)
    elif raw_url.startswith("postgres://"):
        url = raw_url.replace("postgres://", "postgresql+psycopg://", 1)
    else:
        raise RuntimeError("DATABASE_URL debe utilizar PostgreSQL + Psycopg")

    return create_engine(
        url,
        pool_pre_ping=True,
        pool_recycle=1800,
        connect_args={"connect_timeout": 5, "sslmode": "require"},
    )


# ============================================================
# BLOQUE 3: Dependencia de sesión por petición.
# Devuelve un error genérico, sin exponer SQL ni credenciales.
# ============================================================
def get_db() -> Generator[Session, None, None]:
    if not settings.database_url:
        raise HTTPException(status_code=503, detail="Servicio de datos no configurado")

    try:
        factory = sessionmaker(bind=get_engine(), autoflush=False, expire_on_commit=False)
        with factory() as db:
            yield db
    except (SQLAlchemyError, OSError):
        raise HTTPException(
            status_code=503,
            detail="Servicio de datos temporalmente no disponible",
        ) from None
