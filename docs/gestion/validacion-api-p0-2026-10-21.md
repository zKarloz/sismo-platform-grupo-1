# Registro de validación — API P0 contra Supabase

**Proyecto:** Sistema de Monitoreo Sísmico / Sismo Platform

**Fecha:** 2026-10-21

**Rama:** `feature/api-eventos-p0`

**Responsabilidad:** integrante 1 implementó temporalmente los endpoints, por acuerdo con integrante 3.

**Resultado:** **APROBADO EN ENTORNO LOCAL CON SUPABASE REAL**, con las limitaciones especificadas abajo.

## 1. Alcance y arquitectura

- FastAPI, Pydantic 2, SQLAlchemy 2 y Psycopg 3; Python en `.venv` local de `services/api/`.
- PostgreSQL administrado por Supabase, con identificadores UUID.
- Conexión de lectura con rol `sismo_api_reader`, permisos `SELECT` solo en `data_sources` y `seismic_events`, políticas RLS para esas tablas y `BYPASSRLS = false`.
- `DATABASE_URL` en `services/api/.env`; NO registrar secretos en el repositorio ni en este documento.
- Los endpoints devuelven datos consultados de PostgreSQL: **no utilizan eventos sísmicos simulados en la ejecución real**.

## 2. Rutas y evidencias HTTP

| Método | Ruta | Resultado observado |
|---|---|---|
| GET | `/health` | HTTP 200 |
| GET | `/api/v1/status` | HTTP 200 |
| GET | `/api/v1/events` | HTTP 200 |
| GET | `/api/v1/sources` | HTTP 200 |
| GET | `/api/v1/dashboard/summary` | HTTP 200 |
| GET | `/api/v1/events/geojson` | HTTP 200 |
| GET | `/api/v1/events/00000000-0000-0000-0000-000000000001` | HTTP 404 (identificador inexistente) |

La comprobación HTTP automatizada mediante `httpx` terminó con `VALIDACIÓN HTTP: OK`. Se confirmó que Swagger UI se sirve en `/docs` y que Uvicorn inició con `Application startup complete`.

## 3. Evidencia de pruebas y conexión

1. Entorno Python aislado creado en `services/api/.venv/` y dependencias instaladas desde `requirements.txt`.
2. `python -m unittest discover -s tests -p 'test_*.py' -v`: **24 pruebas aprobadas**.
3. Conexión de SQLAlchemy/Psycopg a PostgreSQL: **OK**; `SELECT current_user` devolvió `sismo_api_reader`.
4. Consultas reales: `SELECT COUNT(*) FROM public.data_sources` devolvió **0** y `SELECT COUNT(*) FROM public.seismic_events` devolvió **0**.
5. `git check-ignore -v .env .venv/` confirmó que ambos se excluyen de Git.
6. La advertencia `StarletteDeprecationWarning` fue no bloqueante.

## 4. Estado de las fases

- **API P0 — punto de control completado:** cinco rutas GET implementadas, pruebas locales y conexión real verificadas.
- **Fase 3 — ingesta:** NO finalizada. Falta obtener, validar y normalizar datos IGP/USGS, cargar registros, deduplicar, registrar ejecuciones y medir errores.
- **Fase 4 — dashboard/mapa:** backend P0 validado; NO finalizada. Falta integrarlo con frontend, datos oficiales y escenarios reales.
- **Despliegue:** NO verificado en Render/Vercel, ni se han ejecutado pruebas end-to-end en producción.

## 5. Seguridad y tareas siguientes

- **Acción prioritaria:** rotar cualquier contraseña compartida fuera de los canales privados; si coincide con la contraseña administrativa del proyecto, coordinar el cambio con el equipo.
- No subir `services/api/.env`, directorios `.venv/`, cadenas de conexión, contraseñas, `__pycache__/` ni archivos generados.
- Mantener el rol de lectura sin permisos de escritura ni `BYPASSRLS`.
- Auditar y restringir los permisos excesivos previamente detectados en `anon` y `authenticated`, incluido `TRUNCATE`, antes de exponer servicios a terceros.
- Revisar el modo TLS y la verificación de certificados para producción. Confirmar secretos en el servicio de despliegue.
- Alinear las migraciones aplicadas manualmente con el historial de Alembic antes de ejecutar migraciones automatizadas.
- Obtener revisión del integrante 3 y del líder antes de fusionar la rama con `develop`.

## 6. Criterio de aceptación del hito

**Cumplido:** los cinco endpoints GET P0 responden HTTP 200 contra la base de datos real vacía, el detalle inexistente responde 404, y los 24 tests aprobados no presentan regresiones. Esto **no valida todavía** la ingesta, las estadísticas con datos oficiales o el modelo predictivo.
