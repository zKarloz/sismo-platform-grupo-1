# Fase 04 — Dashboard y mapa sísmico (avance técnico parcial)

> **Estado:** EN DESARROLLO — NO CERRADA.

> **Fecha de última validación:** 2026-10-21.

> **Responsable temporal del backend:** integrante 1, coordinado con integrante 3.

> **Plan:** PDF del proyecto, dashboard, mapa y análisis descriptivo.

## 1. Funcionalidad backend implementada

| Método | Endpoint                    | Contrato principal                                                         |
| ------ | --------------------------- | -------------------------------------------------------------------------- |
| GET    | `/api/v1/dashboard/summary` | `total_events`, `latest_event_at`, `average_magnitude`, `average_depth_km` |
| GET    | `/api/v1/events/geojson`    | Colección de entidades GeoJSON `FeatureCollection`                         |

Los dos servicios aplican filtros por rango temporal, magnitud y fuente, validados en `app/routers/event_filters.py`. GeoJSON dispone además de `limit` y `offset`, ordena coordenadas como `[longitud, latitud]` y excluye eventos sin coordenadas válidas. Se registra la ruta estática `/geojson` antes de la ruta dinámica `/{event_id}`.

Archivos principales: `app/routers/dashboard.py`, `app/routers/events.py`, `app/repositories/dashboard.py`, `app/repositories/geojson.py`, `app/schemas/dashboard.py`, `app/schemas/geojson.py`, `tests/test_dashboard_geojson.py`.

## 2. Evidencia de validación

- **24 pruebas automatizadas del backend aprobadas**, incluidas las pruebas del dashboard y GeoJSON con SQLite aislado.
- Uvicorn inició y Swagger UI se mostró en `/docs`.
- Prueba HTTP real contra PostgreSQL/Supabase: **200** para `/api/v1/dashboard/summary` y **200** para `/api/v1/events/geojson`.
- El rol `sismo_api_reader` consiguió consultar PostgreSQL; el catálogo tiene **0 fuentes y 0 eventos** al momento de verificar.
- Detalle de la evidencia en `docs/gestion/validacion-api-p0-2026-10-21.md`.

## 3. Pendientes para cerrar la Fase 4

- Conectar los endpoints al frontend React/Tailwind/Lucide del integrante 2.
- Comprobar gráficas, tarjetas KPI, mapa, filtros y estados de carga/error/vacío con la UI real.
- Importar catálogo sísmico oficial mediante la Fase 3 y verificar cifras/mapas con eventos reales.
- Validar paginación, zonas horarias, precisión numérica y tiempos de respuesta con datos representativos.
- Verificar Render/Vercel, CORS por dominio final y TLS antes del despliegue.
- Revisar seguridad, accesibilidad, integración y PR con el grupo.

**Nota científica:** estadísticas descriptivas de actividad sísmica no constituyen pronósticos de terremotos ni alertas oficiales.

**Conclusión:** backend P0 de dashboard/mapa validado; la fase integral **no está terminada**.
