"""Punto de entrada HTTP del backend FastAPI (Fase 1)."""

# ============================================================
# 1. IMPORTACIONES Y CONFIGURACIÓN
# ============================================================
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings


# ============================================================
# 2. APLICACIÓN PRINCIPAL Y DOCUMENTACIÓN OPENAPI
# ============================================================
app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description=(
        "API del sistema de monitoreo sísmico. "
        "Durante la Fase 1 expone únicamente comprobaciones técnicas."
    ),
)


# ============================================================
# 3. CORS PARA EL FRONTEND (LOCAL Y VERCEL)
# No permite todos los orígenes indiscriminadamente.
# ============================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


# ============================================================
# 4. RUTAS DEL ESTADO DEL SERVICIO
# Importante: /health comprueba la API, NO Supabase.
# ============================================================
@app.get("/health", tags=["Sistema"])
def health_check() -> dict[str, str]:
    """Comprobación de vida para local, Docker y Render."""
    return {"status": "ok", "service": "sismo-api"}


@app.get(f"{settings.api_v1_prefix}/status", tags=["Sistema"])
def api_status() -> dict[str, str]:
    """Verifica que el prefijo versionado funciona."""
    return {"status": "ok", "api_version": "v1"}
