# Fase 03 — Contrato preliminar de persistencia e idempotencia IGP

**Proyecto:** Sismo Platform — Sistema de Monitoreo Sísmico  
**Fecha:** 22/10/2026  
**Rama de trabajo:** `feature/ingesta-eventos-p0`  
**Estado:** **DISEÑO Y SIMULACIÓN LOCAL VALIDADA — NO APROBADO PARA SUPABASE**.

## 1. Antecedentes y fuente de verdad

- Fuente: archivo `datos-sismicos_Instrumental_1960-01-01_2026-10-21.xlsx` (IGP).
- SHA-256: `8dde2a7eb250ec1ff99a2df495918b347de1281420c1f625d1a5eeabf1120d9a`.
- Esquema de referencia: `database_tables_definition_2110_2.txt` aportado por el equipo, con cuatro tablas UUID.
- Existente: normalizador `services/ingestion/igp/normalizer.py`, lector `reader.py` y `dry_run.py`, **8 pruebas previas aprobadas**.
- Explorado en Jupyter: 21 pares próximos con 41 filas involucradas; son **candidatos de revisión**, no duplicados confirmados.
- El esquema de referencia **no demuestra por sí solo** el estado vivo de permisos RLS, el historial Alembic, registros preexistentes ni la disponibilidad del rol escritor.

## 2. Archivos nuevos de esta entrega

| Archivo | Alcance |
|---|---|
| `services/ingestion/igp/persistence_plan.py` | Planificador completamente local, clasifica insertar / omitir / inválido, preservando la representación de origen para staging |
| `services/ingestion/tests/test_persistence_plan.py` | Seis pruebas adicionales de clasificación y doble ejecución |
| `docs/gestion/propuestas-sql/20261022_igp_record_fingerprint_REVISION_NO_EJECUTAR.sql` | Inspecciones SQL de solo lectura y propuesta de cambios **comentada, no ejecutable por accidente** |
| `docs/gestion/avance-fase03-plan-persistencia-igp-2026-10-22.md` | Este registro técnico |

Esta entrega **no reemplaza** el contenido de `services/ingestion/`, `database/` ni `docs/fases/fase-02-diseno-datos.md`.

## 3. Contrato de identidad propuesto

Distinguir tres identificadores que **no son intercambiables**:

1. `file_sha256`: identidad de la descarga XLSX.
2. `record_fingerprint`: SHA-256 de los parámetros sísmicos normalizados (algoritmo actual `igp-record-v1`): identifica **versión exacta del registro**, no un terremoto físico estable.
3. `external_id`: identificador oficial por evento; **no disponible en el XLSX**; mantener `NULL` hasta verificar si existe.

En `seismic_events`, proponer columna nullable `record_fingerprint` e índice único parcial `(source_id, record_fingerprint)` solo cuando ambos no sean `NULL`, con formato SHA-256 lowercase y fuente obligatoria si hay huella.

**Advertencia:** si el IGP publica parámetros revisados, la huella cambia y puede aparecer un nuevo candidato. No fusionar automáticamente por proximidad. La unicidad por huella es un mecanismo de idempotencia **exacta**, no deduplicación científica entre ediciones.

## 4. Contrato de almacenamiento posterior (sin implementar)

| Tabla | Flujo futuro |
|---|---|
| `data_sources` | Resolver el UUID de la fuente IGP antes de comenzar; no inventarlo |
| `ingestion_runs` | Una fila por intento, con estado y contadores `records_seen`, `records_inserted`, `records_updated`, `records_skipped`, `records_failed` |
| `seismic_events_staging` | Una fila por registro de entrada **en cada ejecución**, incluidas las inválidas y repetidas; `raw_payload` JSONB con `provider`, `file_sha256`, `excel_row`, `fingerprint_version`, `record_fingerprint`, `raw`; `validation_errors` estructurados |
| `seismic_events` | Solo para registros válidos y no insertados previamente; columnas normalizadas y huella exacta |

Estados de staging **propuestos y pendientes de aprobación**: `valid`, `invalid`, `duplicate`. En la implementación definitiva, determinar el estado luego de confirmar el resultado de `INSERT ... ON CONFLICT ... DO NOTHING RETURNING id`, no solo por la memoria del planificador.

El contador `records_seen` debe reconciliar con `records_inserted + records_updated + records_skipped + records_failed` para cada ejecución. `records_updated = 0` mientras no exista una política de revisiones.

Para cada lote, usar una transacción consistente y evitar un estado en staging marcado como insertado antes de confirmar la escritura canónica. Gestionar fallos por lote y cerrar/registrar la ejecución sin perder el error. La elección de tamaño de lote y la retención deben revisarse con el integrante 4.

## 5. Seguridad antes de Supabase

- **No** modificar `sismo_api_reader`: permanece exclusivamente de lectura.
- Diseñar rol de ingesta independiente con permisos mínimos y políticas RLS explícitas; verificar también privilegios sobre esquema, tablas y funciones usadas.
- Prohibido usar secretos de Supabase en notebooks, código o evidencias.
- Revisar estructura real, migraciones manuales y Alembic; **NO ejecutar** `database/migrations/20261020_001_esquema_monitoreo_sismico.sql` sobre esquema UUID.
- Obtener autorización explícita antes de crear columnas, índices, roles, políticas, fuentes o realizar escrituras.
- Las pruebas de doble ejecución local **no validan concurrencia ni atomicidad** en PostgreSQL. Una restricción UNIQUE aprobada y pruebas de integración serán necesarias.

## 6. Pruebas y evidencia de la simulación

Comandos desde `services/ingestion`, con `.venv-data` activado:

```bash
# =====================================================
# BLOQUE 1: Pruebas existentes y nuevas (solo locales).
# =====================================================
python -m unittest discover -s tests -p 'test_*.py' -v

# =====================================================
# BLOQUE 2: Dos pasadas del mismo XLSX sin Supabase.
# =====================================================
python -m igp.persistence_plan \
  --input '../../data/raw/datos-sismicos_Instrumental_1960-01-01_2026-10-21.xlsx' \
  --output '../../data/reports/igp-plan-persistencia-2026-10-22.json'
```

### Resultado observado en entorno aislado

| Métrica | Primera pasada | Segunda pasada |
|---|---:|---:|
| Registros inspeccionados | 25.799 | 25.799 |
| Candidatos a staging | 25.799 | 25.799 |
| Candidatos a INSERT | **25.799** | **0** |
| Omitidos por huella exacta | 0 | **25.799** |
| Registros inválidos | 0 | 0 |

Pruebas unitarias de los módulos combinados: **14/14 aprobadas** (8 existentes y 6 nuevas). El informe local declara `database_writes: false`.

**Interpretación correcta:** son *decisiones de simulación* usando memoria local. **No son registros insertados ni contadores reales de Supabase**.

## 7. Estado para la siguiente etapa

- [x] Explorar y validar XLSX del IGP.
- [x] Ejecutar normalizador y `dry-run` original.
- [x] Simular primera importación y reimportación exacta sin BD.
- [x] Preparar propuesta mínima de identidad para revisión.
- [ ] Revisar el SQL y aprobar estrategia con integrante 4/líder.
- [ ] Verificar el estado real de esquema, RLS y Alembic.
- [ ] Implementar y probar adaptador PostgreSQL **en base de ensayo**, transacciones y concurrencia.
- [ ] Autorizar primer lote pequeño en Supabase y contrastar API de lectura.

**La Fase 3 sigue EN DESARROLLO.** Este documento es evidencia del avance, no acta de cierre.
