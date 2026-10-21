"""Punto de entrada HTTP del backend FastAPI (Fases 1 y 3)."""

# ============================================================
# BLOQUE 1: Importaciones y configuración.
# ============================================================
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers.dashboard import router as dashboard_router
from app.routers.events import router as events_router
from app.routers.sources import router as sources_router


# ============================================================
# BLOQUE 2: Aplicación principal y documentación OpenAPI.
# ============================================================
app = FastAPI(
    title=settings.app_name,
    version="0.2.0",
    description=(
        "API de monitoreo sísmico. Incluye rutas técnicas de Fase 1 "
        "y rutas P0 de eventos, fuentes, dashboard y mapa en desarrollo."
    ),
)


# ============================================================
# BLOQUE 3: CORS para frontend (local y Vercel).
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
# BLOQUE 4: Rutas existentes de Fase 1.
# /health NO verifica la conexión a Supabase.
# ============================================================
@app.get("/health", tags=["Sistema"])
def health_check() -> dict[str, str]:
    """Comprobación de vida para local, Docker y Render."""
    return {"status": "ok", "service": "sismo-api"}


@app.get(f"{settings.api_v1_prefix}/status", tags=["Sistema"])
def api_status() -> dict[str, str]:
    """Verifica que el prefijo versionado funciona."""
    return {"status": "ok", "api_version": "v1"}


# ============================================================
# BLOQUE 5: Routers de lectura P0.
# ============================================================
app.include_router(events_router)
app.include_router(sources_router)
app.include_router(dashboard_router)
