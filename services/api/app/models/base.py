"""Base declarativa compartida de los modelos ORM de lectura."""

# ============================================================
# BLOQUE 1: Base de SQLAlchemy.
# Nunca se ejecuta create_all() sobre Supabase desde la API.
# ============================================================
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
