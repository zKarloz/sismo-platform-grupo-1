# Fase 3 — Normalizador local del catálogo IGP

> **Estado:** etapa de implementación y pruebas locales; NO es una ingesta a Supabase.

## 1. Alcance

- Lectura **sin modificar** el Excel `IGP - Datos sísmicos`, con validación estricta de seis columnas.
- Normalización de fecha y hora UTC; latitud, longitud, profundidad (km) y magnitud.
- Registro de errores estructurados por fila (compatible conceptualmente con `validation_errors JSONB`).
- Huella SHA-256 reproducible de la **versión del registro** y detección de coincidencias exactas.
- Vista previa del contrato de `seismic_events`, manteniendo `external_id` y otros campos ausentes como `None`.
- Informe local resumido sin escritura a Supabase; **no usa credenciales ni se conecta a PostgreSQL**.

**No implementado:** política definitiva de identidad entre versiones, staging persistente, `ingestion_runs` reales, permisos de escritura, Alembic, sincronización incremental ni idempotencia en PostgreSQL. Los 21 pares encontrados en Jupyter siguen siendo **candidatos a revisión**, no duplicados confirmados.

## 2. Preparación en Windows + Git Bash

**Desde la raíz** `sismo-platform-grupo-1-definitivo`, con `.venv-data` ya creado:

```bash
# =====================================================
# BLOQUE 1: Activar entorno de análisis existente.
# =====================================================
source .venv-data/Scripts/activate

# =====================================================
# BLOQUE 2: Instalar solo lo necesario para la ingesta.
# =====================================================
python -m pip install -r services/ingestion/requirements.txt

# =====================================================
# BLOQUE 3: Comprobar exclusiones antes de agregar archivos.
# Si falta alguna regla, incorporarla conscientemente a .gitignore.
# =====================================================
git check-ignore -v .venv-data/ data/raw/ data/reports/ || true

# =====================================================
# BLOQUE 4: Acceder al módulo de ingesta.
# =====================================================
cd services/ingestion
```

## 3. Pruebas unitarias

**Desde `services/ingestion`:**

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
```

## 4. Dry-run completo del Excel IGP

**Desde `services/ingestion`:**

```bash
python -m igp.dry_run \
  --input '../../data/raw/datos-sismicos_Instrumental_1960-01-01_2026-10-21.xlsx' \
  --output '../../data/reports/igp-dry-run-2026-10-22.json'
```

`--output` es opcional. Crea solo un **informe JSON local**, no una exportación de eventos ni inserciones en base de datos. El programa devuelve código 2 si hay registros inválidos y código 1 ante problemas de lectura o contrato.

## 5. Evidencias que esperamos comprobar

| Métrica | Referencia del notebook | Debe verificarse con el dry-run |
|---|---:|---|
| Registros | 25.799 | Sí |
| Nulos y errores de rango | 0 | Sí |
| Huellas exactas repetidas | 0 | Sí |
| Eventos en 2024 | 556 | Sí |
| Pares próximos | 21 | No se recalculan: auditoría exploratoria separada |

**No usar la huella como `external_id` sin revisión:** representa parámetros de un registro en una versión del catálogo y cambia si el IGP revisa un evento. Los UUID de Supabase no se generan aquí.

## 6. Seguridad y Git

- No incluir `.env`, `.venv-data/`, archivos originales privados o informes generados en commits por defecto.
- Confirmar reglas de `.gitignore` para `data/raw/`, `data/reports/`, `.venv-data/` antes de `git add`.
- No ejecutar la migración SQL antigua `database/migrations/20261020_001_esquema_monitoreo_sismico.sql` contra la base UUID actual.
- Respetar archivos existentes de otros integrantes. Preparar cambios únicamente con `git add` de rutas explícitas.
