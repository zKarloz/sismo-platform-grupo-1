# Fase 03 — Revisión preliminar de la fuente histórica IGP

> **Proyecto:** Sismo Platform — Sistema de Monitoreo Sísmico  
> **Fecha de revisión:** 2026-10-21  
> **Estado:** Inspección documental y de calidad COMPLETADA; ingesta NO EJECUTADA; Fase 3 EN DESARROLLO.  
> **Fuente:** Instituto Geofísico del Perú (IGP), Centro Sismológico Nacional (CENSIS).  
> **Advertencia:** Esta es una inspección del archivo local y la ficha oficial, no una certificación científica de cada evento.

## 1. Archivos revisados

- `IGP_catalogo_sismico_1960_ 2025_Dataset.csv`: archivo fuente semiestructurado delimitado por punto y coma (`;`).
- `IGP_catalogo_sismicos_desde_1960_ DiccionarioDatos.xlsx`: hoja `DiccionarioDatos`, con significado y tipos de campos.
- `IGP_catalogo_sismicos_desde_1960_ Metadatos_0.docx`: metadatos de procedencia y licencia.

## 2. Procedencia y condiciones de reutilización

- Portal oficial: https://www.datosabiertos.gob.pe/dataset/cat%C3%A1logo-s%C3%ADsmico-desde-1960-instituto-geof%C3%ADsico-del-per%C3%BA-igp
- Recurso CSV: https://www.datosabiertos.gob.pe/dataset/catalogo-sismico/resource/f9629081-0721-4101-a2c2-d0622e046f8b
- Entidad publicadora: Instituto Geofísico del Perú (IGP).
- Fuente identificada en metadatos: CENSIS.
- Cobertura declarada: Perú, 1960–2025.
- Frecuencia declarada: anual; **no debe etiquetarse como flujo de tiempo real**.
- Versión en DOCX: 2.0; última actualización informada: 2026-05-26 12:00 UTC-05:00.
- Ficha de portal: fecha de modificación 2026-06-15.
- Licencia declarada en metadatos y ficha oficial consultada: Open Data Commons Attribution License (ODC-BY).
- Licencia y atribución: https://opendatacommons.org/licenses/by/1-0/
- Conservar en visualizaciones/publicaciones: nombre de fuente, enlace al catálogo, versión/fecha consultada, indicación de transformaciones y referencia a la licencia.
- **No asumir** que esta publicación concede acceso programático a reportes recientes de CENSIS.

## 3. Resultado de inspección local del CSV

| Indicador                               | Valor                                                              |
| --------------------------------------- | ------------------------------------------------------------------ |
| Registros de datos                      | 24,289                                                             |
| Columnas                                | 8                                                                  |
| Tamaño exacto (bytes)                   | 1,318,883                                                          |
| SHA-256                                 | `72ce039181bb42ce04f2fd3369c17eeecf7f7fa01f65b8e8c8816be4217c0f86` |
| Primer año de evento                    | 1960                                                               |
| Último año de evento                    | 2025                                                               |
| Registros de 2024                       | 0                                                                  |
| Registros de 2025                       | 609                                                                |
| Campos vacíos observados                | 0                                                                  |
| Filas con hora de menos de 6 caracteres | 11,034                                                             |
| Grupos con datos sísmicos idénticos     | 8                                                                  |
| Filas adicionales en dichos grupos      | 8                                                                  |
| IDs duplicados dentro del archivo       | 0                                                                  |

**Cabecera:** `ID;FECHA_UTC;HORA_UTC;LATITUD;LONGITUD;PROFUNDIDAD;MAGNITUD;FECHA_CORTE`.

Las fechas de evento se pueden interpretar como `aaaammdd` y horas UTC como `hhmmss`, completando ceros a la izquierda. Esta operación debe probarse contra el diccionario y fixtures antes de importar.

## 4. Hallazgos / alertas de calidad

1. **Vacío temporal de 2024:** el CSV no incluye registros fechados en 2024, aunque contiene eventos de 2023 y 2025. Esto no significa que no hayan ocurrido sismos en 2024. Requiere contrastar la versión publicada y/o preguntar al IGP.
2. **Ocho pares de registros indistinguibles por atributos sísmicos:** tienen distinta columna `ID`, pero igual fecha, hora, latitud, longitud, profundidad y magnitud. Son **candidatos a duplicados**, no correcciones automáticas. Deben aislarse y revisarse.
3. **`FECHA_CORTE` inconsistente con el formato declarado `aaaammdd`:** se observaron los valores `20223006` (22712), `20260528` (609), `20231910` (501), `20240101` (467). Dos valores no son fechas válidas bajo `aaaammdd`; parecen emplear una convención distinta de día/mes, pendiente de verificación. **No convertir automáticamente** esta variable ni utilizarla como fecha del sismo.
4. **Hora sin ceros de la izquierda:** 11,034 filas guardan la hora en menos de seis caracteres; la normalización debe usar `zfill(6)`.
5. **Identificadores internos:** el campo `ID` va consecutivamente desde 0 hasta 24288. El diccionario no lo define; por ello no se ha demostrado que identifique un sismo de modo estable entre versiones. No establecer todavía `UNIQUE(source_id, external_id)` usando directamente este número.
6. **Unidades:** el diccionario declara magnitud en escala Mw y fecha/hora UTC; describe la profundidad pero **no explicita su unidad**. Confirmar unidad antes de mapear `PROFUNDIDAD` a `depth_km`.
7. **Atributos ausentes:** el CSV no ofrece localidad (`place`) ni URL específica por evento. No fabricar datos; usar `NULL` cuando corresponda y conservar como procedencia el enlace al catálogo, diferenciado de un enlace a informe individual.
8. **Metadatos internos desactualizados:** DOCX/XLSX contienen en el título “1960–2023”, pero describen/acompañan una cobertura hasta 2025. Guardar ambos valores y aclararlo en documentación.
9. **Cobertura variable:** la ficha del IGP indica que la Red Sísmica Nacional mejoró su cobertura desde 2000; comparar cifras históricas por año requiere advertir cambios de detectabilidad/cobertura.

## 5. Mapeo provisional hacia Supabase

| Archivo IGP              | PostgreSQL / regla                                                          |
| ------------------------ | --------------------------------------------------------------------------- |
| Fuente IGP/CENSIS        | `data_sources` (registrar el proveedor y URL del catálogo)                  |
| `ID`                     | Campo de origen provisional; **no prometer estabilidad** como `external_id` |
| `FECHA_UTC` + `HORA_UTC` | `seismic_events.occurred_at` (`timestamptz` UTC)                            |
| `LATITUD`, `LONGITUD`    | `latitude`, `longitude` (con validación de rangos)                          |
| `MAGNITUD`               | `magnitude`, `magnitude_type='Mw'` según diccionario                        |
| `PROFUNDIDAD`            | `depth_km` **solo tras confirmar km**                                       |
| `FECHA_CORTE`            | Metadato de versión/corte para ingesta; no equivale a `occurred_at`         |
| Cada fila original       | `seismic_events_staging.raw_payload`                                        |
| Validaciones             | `seismic_events_staging.validation_errors` y estado                         |
| Resultado de la carga    | `ingestion_runs` (conteos, fallos, procedencia)                             |

## 6. Próximos pasos sin alterar Supabase

1. Conservar una copia inmutable del CSV original y su SHA-256.
2. Crear fixtures de fecha/hora UTC, errores de `FECHA_CORTE`, 2024 ausente y los ocho pares repetidos.
3. Acordar con el equipo el identificador estable y la política de deduplicación/idempotencia antes de crear restricciones.
4. Preparar parser en `services/ingestion` con modo `--dry-run` y reporte de calidad.
5. Revisar la diferencia entre el modelo Supabase UUID real y la antigua migración SQL, **sin ejecutarla**.
6. Validar política RLS/rol escritor separado y obtener autorización antes de cualquier inserción.
7. Actualizar `docs/fases/fase-03-ingesta-eventos.md` con evidencias verificables; no declarar cerrada la fase todavía.

**Conclusión:** el CSV histórico IGP es una fuente legítima y aprovechable para el MVP académico, pero requiere depuración documentada y controles de calidad antes de ser persistido en Supabase.
