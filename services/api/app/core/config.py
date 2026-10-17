"""Configuración centralizada para FastAPI (Fase 1)."""

# ============================================================
# 1. IMPORTACIONES Y RUTA DEL ENTORNO LOCAL
# ============================================================
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Funciona al ejecutar desde la carpeta api y dentro de Docker.
ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


# ============================================================
# 2. ESQUEMA TIPADO DE CONFIGURACIÓN
# ============================================================
class Settings(BaseSettings):
    """Variables de entorno permitidas; no imprimir secretos."""

    app_name: str = "Sistema de Monitoreo Sísmico | API"
    app_env: str = "development"
    api_v1_prefix: str = "/api/v1"
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    database_url: str = ""  # Reservada para integrar Supabase en fases posteriores.

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def allowed_origins(self) -> list[str]:
        """Convierte los orígenes separados por comas en una lista."""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


# ============================================================
# 3. INSTANCIA GLOBAL (SIN ABRIR CONEXIONES A LA BASE DE DATOS)
# ============================================================
settings = Settings()
