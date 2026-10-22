# Diagnóstico técnico de continuidad — Sismo Platform

**Fecha de revisión:** 2026-10-21  
**Actividad:** Fase 3, Etapa 1 — Revisión técnica (sin cambios a Supabase ni al repositorio).  
**Estado del diagnóstico:** Revisión documental completada; comprobaciones operativas pendientes.  
**Referencia:** plan de desarrollo, backlog académico, fases 0–4, definición SQL suministrada y evidencia de API P0.

## 1. Resumen ejecutivo

La API REST P0 existe en `develop` y no requiere reconstrucción. El PR #4 se fusionó el 21/10/2026, con `bc23369` y merge `62bf836`; GitHub muestra cuatro checks aprobados y ninguna revisión formal. El reporte `validacion-api-p0-2026-10-21.md` es una evidencia histórica sustancialmente coherente, pero no certifica que hoy estén disponibles la base de datos, los datos o el despliegue de producción.

El archivo `database_tables_definition_2110_2.txt` es el **referente documental del esquema suministrado más reciente**; no es una conexión en vivo. Describe 4 tablas con UUID, 5 FK, 4 CHECK, una restricción UNIQUE compuesta, 7 índices explícitos y 5 índices implícitos derivados de 4 PK y una UNIQUE: **12 índices esperados**. El documento `fase-02-diseno-datos.md` sigue describiendo el diagnóstico antiguo con `bigint`, tres tablas y falta de claves foráneas. Debe actualizarse conservando su historia; la migración antigua no se ejecutará sobre el esquema UUID vigente.

No se efectuaron escrituras, migraciones, conexiones autenticadas a Supabase ni pruebas locales.

## 2. Estado documental por fase

| Fase / hito                         | Estado defendible                                                 | Reserva                                                                                                    |
| ----------------------------------- | ----------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| Fase 0 — Alcance                    | Cierre de planificación condicionado                              | Ratificación del equipo pendiente según acta.                                                              |
| Fase 1 — Base técnica               | Cerrada bajo alcance académico reducido                           | Esquema y seguridad empresarial se transfirieron a otras fases.                                            |
| Fase 2 documental — Diseño de datos | Documento desactualizado; no cerrar sin actualización y evidencia | El número coincide con la Fase 2 del PDF, dedicada a identidad/permisos: aclarar la nomenclatura.          |
| API P0 — Lectura                    | Hito integrado en `develop`                                       | 24 tests y 7 HTTP son evidencias registradas, no pruebas repetidas durante esta revisión.                  |
| Fase 3 — Ingesta                    | En desarrollo                                                     | Sin conector, normalizador, staging, persistencia ni prueba de idempotencia de eventos reales confirmados. |
| Fase 4 — Dashboard/mapa             | En desarrollo                                                     | Backend de resumen y GeoJSON implementado; falta interfaz con datos reales.                                |

## 3. Esquema suministrado para Supabase

| Tabla                    | Función y campos relevantes                                                                                                                 | Observaciones                                                                                        |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `data_sources`           | `id uuid`, `name`, `base_url`, `source_type`, `status`, `last_sync_at`, `config_ref`                                                        | Las fuentes seguían vacías cuando se registró la validación anterior; no extrapolar a hoy.           |
| `ingestion_runs`         | `id uuid`, `source_id uuid`, estado, tiempos, 5 contadores y resumen de error                                                               | CHECK de contadores no negativos y orden de fechas; UNIQUE (`id`, `source_id`) permite FK compuesta. |
| `seismic_events`         | `id uuid`, `source_id uuid`, `external_id`, hora UTC, coordenadas, magnitud, profundidad, procedencia, `received_at`, `review_status`       | CHECK de latitud y longitud; **no existe UNIQUE (`source_id`, `external_id`)**.                      |
| `seismic_events_staging` | `id uuid`, `source_id uuid`, `ingestion_run_id uuid`, `external_id`, `raw_payload jsonb`, estado, `validation_errors jsonb`, `processed_at` | Tres FK, incluida una compuesta; sus campos de referencia son nullable.                              |

**Precisión:** el archivo de definiciones de tablas no incluye políticas RLS, GRANT/REVOKE, usuarios o `pg_indexes` reales. Por tanto, no prueba que los permisos y políticas permanezcan activos. Esos aspectos constan en el reporte previo y deben verificarse de solo lectura antes de habilitar escrituras.

## 4. Desactualizaciones documentales detectadas

### `fase-02-diseno-datos.md` — actualización prioritaria

- Actualizar la fotografía histórica de `bigint` y tres tablas; el archivo SQL aportado describe **UUID** y cuatro tablas.
- El staging, cinco FK y cuatro CHECK están presentes en el SQL suministrado, a diferencia de afirmaciones iniciales.
- Los campos geográficos y numéricos actuales se declaran `numeric` sin precisión fija; no presentarlos como `numeric(9,6)`, `numeric(5,2)` o `numeric(8,3)` efectivos.
- El texto «migración no ejecutada» se debe mantener únicamente si se refiere de modo inequívoco al archivo antiguo de migración propuesto. Documentar por separado los cambios manuales posteriores a UUID.
- Actualizar estado, criterios de cierre, diagrama, decisiones de seguridad y compatibilidad con Alembic.
- No ejecutar `database/migrations/20261020_001_esquema_monitoreo_sismico.sql` sobre la base UUID actual.

### `validacion-api-p0-2026-10-21.md` — válido como acta histórica, incompleto como estado actual

- Conservar la rama de origen `feature/api-eventos-p0` y **añadir** que el PR #4 quedó fusionado en `develop`, commit `62bf836`, el 21/10/2026.
- Cambiar «obtener revisión antes de fusionar» por una nota histórica: la integración ya ocurrió y GitHub mostraba «No reviews» al consultar el PR.
- Etiquetar «0 fuentes y 0 eventos», 24 tests, 7 respuestas HTTP y `current_user=sismo_api_reader` como _resultados de la sesión documentada_, no como resultados de una reconexión de hoy.
- Aclarar que los checks de CI no prueban una consulta real a Supabase si no hay credenciales de producción en CI.
- Mantener la advertencia «despliegue de la API P0 no verificado en producción» aunque la infraestructura básica estuviera desplegada desde Fase 1.
- Agregar referencia a hash del commit probado, fecha/hora, entorno y enlaces de evidencias si están disponibles.

### `fase-03-ingesta-eventos.md` y `fase-04-dashboard-mapa.md`

- Ambos indican correctamente «EN DESARROLLO — NO CERRADA».
- Cambiar «actualmente 0 registros» por «0 registros al momento de validación».
- Mantener separación entre rutas P0 comprobadas y funciones de ingesta/frontend pendientes.

## 5. Riesgos y controles de diseño

| Riesgo                        | Evidencia / causa                                                                                    | Control propuesto                                                                                                                                          |
| ----------------------------- | ---------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Duplicados                    | Ausencia de UNIQUE (`source_id`, `external_id`)                                                      | Verificar estabilidad de ID USGS; usar comprobación lógica en pruebas, estudiar índice único y tratamiento de concurrencia antes de escritura real.        |
| Integridad parcial de staging | `source_id` y `ingestion_run_id` admiten NULL, y la FK compuesta no comprueba filas con valores NULL | Exigir ambas referencias para staging operativo desde la aplicación; registrar excepciones justificadas.                                                   |
| Privilegios / RLS             | `sismo_api_reader` es de lectura; definiciones SQL no incluyen políticas RLS                         | Usar credencial separada de escritura con privilegios mínimos; verificar `GRANT`, RLS y políticas. No usar cuenta administradora como conexión de ingesta. |
| Migraciones inconsistentes    | Esquema UUID aplicado manualmente y migración antigua tipo `bigint`                                  | Proponer baseline de Alembic reconciliado con esquema real; prohibir autogenerate o upgrade hasta revisión.                                                |
| Calidad de datos              | Campos de magnitud y profundidad pueden ser NULL, valores fuera de rango o distintos por proveedor   | Normalizar UTC y unidades, controlar lat/lon, conservar payload y errores estructurados; no inventar magnitudes.                                           |
| Procedencia / cobertura       | IGP histórico y USGS reciente no equivalentes                                                        | Registrar fuente, ID, URL, fecha de extracción y alcance geográfico; no fusionar eventos entre proveedores automáticamente.                                |
| TLS / secretos                | `sslmode=require` cifra conexión pero no equivale a validar identidad del servidor                   | Diseñar verificación de certificado en despliegue, rotación de credenciales divulgadas y variables separadas.                                              |
| Revisión de equipo            | PR #4 fusionado sin revisión formal visible                                                          | Obtener revisión cruzada de la ingesta y su documentación antes del próximo PR.                                                                            |

## 6. Arquitectura modular propuesta para la Fase 3

Mantener los cinco GET de la API P0 en `services/api`. Crear módulos nuevos en el área de ingesta prevista por el plan, sin alterar contratos de lectura:

```text
services/ingestion/
├── core/                 # Configuración segura y conexión de escritura propia
├── providers/            # Cliente de USGS (posteriormente adaptador de CSV IGP)
├── contracts/            # Contrato de origen, tipos y mapeos versionados
├── normalizers/          # UTC, magnitud, profundidad, coordenadas, nulos
├── validators/           # Calidad y errores estructurados para staging
├── repositories/         # data_sources, ingestion_runs, staging, seismic_events
├── pipelines/            # Orquestación por lote y dry-run
├── tests/                # Fixtures, tests de transformación y duplicados
└── cli.py                # Invocación manual protegida; no endpoint público de sync
```

Secuencia prevista (NO implementada):

1. Consulta controlada a USGS GeoJSON con ventana acotada.
2. Preservación de payload original y metadatos de fuente.
3. Validación y normalización local con errores JSON estructurados.
4. `dry-run` y resultados reproducibles sin escritura.
5. Tras autorización: crear `ingestion_runs`, registrar staging, persistir únicamente eventos válidos usando cuenta de escritura mínima, cerrar ejecución con contadores.
6. Repetir el mismo lote para comprobar idempotencia y verificar los cinco GET ya existentes.

**Separación de conexiones:** la API sigue utilizando `DATABASE_URL` y `sismo_api_reader` para lecturas. La ingesta utilizaría una variable privada diferente (por ejemplo `INGESTION_DATABASE_URL`) y un rol dedicado, **pendiente de diseño y autorización**.

## 7. Primer paso práctico verificable (sin escribir en Supabase)

**Ubicación:** Git Bash, raíz del repositorio local `sismo-platform-grupo-1-ventura`.

```bash
# BLOQUE 1: Confirmar rama, historial y ausencia de cambios accidentales.
pwd
git branch --show-current
git status --short --branch
git log -3 --oneline

# BLOQUE 2: Inspeccionar archivos de ingesta sin modificarlos.
find services/ingestion -maxdepth 3 -type f -print 2>/dev/null || true
find services/api/app/models services/api/tests -maxdepth 2 -type f -print

# BLOQUE 3: Registrar qué migraciones y diagnósticos existen.
find database -maxdepth 3 -type f -print 2>/dev/null || true
```

**Criterio de éxito:** identificar qué existe realmente en la rama `feature/ingesta-eventos-p0`, detectar archivos no rastreados del integrante 4 sin tocarlos y confirmar los módulos ausentes antes de escribir código. No usar `git add .`, `git clean` ni `git reset --hard`.

## 8. Fuentes pendientes de revisión completa

Entre los archivos referidos por el usuario que no se adjuntaron a este análisis están los diagnósticos, diagrama y migración local dentro de `database/`, además del diccionario y CSV IGP. Parte del backend público en `develop` sí se pudo inspeccionar directamente en GitHub; el directorio local de la rama de ingesta no es accesible desde esta revisión. Estas limitaciones no invalidan el diagnóstico documental, pero impiden afirmar que los modelos de ingesta y el historial de migraciones sean idénticos al estado local.

## 9. Decisión para continuar

**No cerrar Fase 2 documental, Fase 3 ni Fase 4 todavía.** Conservar los documentos históricos, preparar una corrección separada de Fase 2, y continuar con un contrato USGS + normalizador probado localmente, sin tocar Supabase hasta que el rol de escritura, deduplicación y SQL estén revisados y expresamente autorizados.

## 10. Referencias

- `Plan_Desarrollo_Sistema_Monitoreo_Sismico_ML.pdf`, pp. 3, 6–9.
- `fase-00-alcance.md`, `fase-01-base-tecnica.md`, `backlog-mvp.md`.
- `fase-02-diseno-datos.md`, `fase-03-ingesta-eventos.md`, `fase-04-dashboard-mapa.md`.
- `database_tables_definition_2110_2.txt`, `validacion-api-p0-2026-10-21.md`.
- GitHub PR #4: https://github.com/zKarloz/sismo-platform-grupo-1/pull/4
- CI: https://github.com/zKarloz/sismo-platform-grupo-1/blob/develop/.github/workflows/ci.yml
- Código de lectura: https://github.com/zKarloz/sismo-platform-grupo-1/tree/develop/services/api
