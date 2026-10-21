# Fase 03 — Ingesta y catálogo de eventos (avance parcial: API P0)

> **Estado:** EN DESARROLLO — NO CERRADA.

> **Fecha de última validación:** 2026-10-21.

> **Responsable temporal de endpoints:** integrante 1, por acuerdo con integrante 3.

> **Plan de referencia:** PDF del proyecto, Fase 3 y backlog de ingesta.

## 1. Alcance del avance implementado

Se implementaron y validaron contra PostgreSQL real de Supabase los endpoints de solo lectura `GET /api/v1/events`, `GET /api/v1/events/{event_id}` y `GET /api/v1/sources`. La lista de eventos admite `limit`, `offset`, fechas con zona horaria, magnitud y fuente. El detalle usa UUID y devuelve 404 ante un identificador inexistente. El catálogo de fuentes no publica `config_ref`.

Los componentes implementados están en `services/api/app/core/database.py`, `models/`, `schemas/`, `repositories/`, `routers/`, `main.py` y `services/api/tests/`. Los archivos nuevos conservan comentarios por bloques.

## 2. Pruebas realizadas

- Dependencias instaladas en el entorno virtual de `services/api/.venv/`.
- **24 de 24 pruebas automatizadas aprobadas** para el backend completo.
- Swagger UI accesible mediante `/docs` y Uvicorn iniciado correctamente.
- **HTTP 200 real** para `/api/v1/events` y `/api/v1/sources` conectado a Supabase.
- **HTTP 404 real** para un UUID de evento inexistente.
- SQLAlchemy/Psycopg se autenticó como `sismo_api_reader`, con acceso solo a `data_sources` y `seismic_events`.
- Ambas tablas tienen actualmente **0 registros**: se valida el comportamiento vacío, no la integridad de un catálogo sísmico importado.
- Detalle completo: `docs/gestion/validacion-api-p0-2026-10-21.md`.

## 3. Seguridad

El rol de la API dispone de permisos `SELECT` sobre las dos tablas públicas requeridas y se encuentra sujeto a RLS (`BYPASSRLS = false`). Los permisos de escritura y `TRUNCATE` del rol fueron verificados como denegados. `.env` y `.venv/` están excluidos por `.gitignore`. Se debe rotar la contraseña divulgada en el chat antes del despliegue y completar la auditoría de privilegios de otros roles.

## 4. Pendientes para cerrar la Fase 3

- Obtener una fuente sísmica oficial comprobable (IGP o USGS), con licencia y atributos definidos.
- Implementar extracción, normalización, registros de staging, validaciones y tratamiento de errores.
- Definir/validar la identidad externa de los eventos y la política de deduplicación.
- Registrar ejecuciones y métricas en `ingestion_runs`; validar sincronización repetida e idempotencia.
- Probar registros reales, fallos y límites del contrato de lectura.
- Integrar migraciones reproducibles con Alembic y revisión por integrantes antes del PR.

**Conclusión:** API de lectura P0 validada; la fase de ingesta **no está terminada**.
