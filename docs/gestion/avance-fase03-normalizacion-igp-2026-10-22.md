# Registro de avance — Fase 03: normalizador IGP y dry-run local

> **Fecha:** 2026-10-22. **Estado de la fase:** EN DESARROLLO — NO CERRADA.
> **Objeto:** registrar el avance sin sustituir `docs/fases/fase-03-ingesta-eventos.md` hasta que se reconcilie con la documentación del equipo.

## 1. Fuentes y respaldo

- Fuente: IGP, repositorio de datos sísmicos instrumentales: https://ultimosismo.igp.gob.pe/repositorio/datos-sismicos
- Entrada: `datos-sismicos_Instrumental_1960-01-01_2026-10-21.xlsx`, hoja `IGP - Datos sísmicos`.
- SHA-256 informado por el notebook: `8dde2a7eb250ec1ff99a2df495918b347de1281420c1f625d1a5eeabf1120d9a`.
- Metadatos complementarios del IGP: versión 2.0 y licencia ODC-BY en documento de metadatos aportado. La licencia y vigencia deben comprobarse antes de publicar una redistribución.

## 2. Resultados comunicados de exploración (Jupyter)

| Control                                  |     Resultado comunicado |
| ---------------------------------------- | -----------------------: |
| Filas                                    |                   25.799 |
| Columnas                                 |                        6 |
| Fechas UTC interpretadas                 |                   25.799 |
| Nulos en campos obligatorios             |                        0 |
| Coordenadas inválidas                    |                        0 |
| Profundidades negativas                  |                        0 |
| Coincidencias exactas en cinco atributos |                        0 |
| Huellas SHA-256 únicas                   |                   25.799 |
| Eventos de 2024                          |                      556 |
| Pares próximos candidatos                | 21 (41 filas implicadas) |

Las tolerancias exploratorias (120 segundos, 20 km, 0,3 de magnitud, 30 km de profundidad) **no demuestran identidad sísmica** y no justifican eliminar filas.

## 3. Implementación propuesta en esta entrega

- `services/ingestion/igp/reader.py`: lectura XLSX solo lectura y verificación de cabecera.
- `services/ingestion/igp/normalizer.py`: validación, UTC, mapeo del evento, errores estructurados y fingerprint reproducible.
- `services/ingestion/igp/dry_run.py`: inspección integral e informe JSON sin conexión a Supabase.
- `services/ingestion/tests/test_igp.py`: pruebas unitarias del contrato y casos de error.
- `services/ingestion/README.md`: instrucciones Git Bash reproducibles.

## 4. Verificación realizada en el entorno de preparación

- **Pruebas automatizadas:** 8/8 exitosas con `unittest` (fixturas sintéticas de prueba).
- **Dry-run completo:** 25.799 filas leídas, 25.799 normalizadas, 0 inválidas y 0 huellas exactas repetidas.
- **Control temporal:** 556 filas en 2024; instante mínimo `1960-01-13T15:40:34+00:00`, máximo `2026-10-21T03:12:48+00:00`.
- **Integridad del archivo:** SHA-256 comprobado `8dde2a7eb250ec1ff99a2df495918b347de1281420c1f625d1a5eeabf1120d9a`.
- **Persistencia:** ninguna; el proceso no utiliza credenciales ni conexiones a Supabase.

Estas comprobaciones se ejecutaron en el entorno de preparación de este paquete. Su ejecución en el equipo local y la revisión conjunta deben registrarse separadamente; no se declara aprobado el CI de GitHub.

## 5. Decisiones que permanecen abiertas

1. Política de identidad estable entre archivos revisados por IGP; `record_fingerprint` NO equivale a `external_id` oficial.
2. Preservación persistente de original + `validation_errors` en staging.
3. Credenciales y RLS para un rol de escritura mínimo, distinto del rol `sismo_api_reader`.
4. Registro de ejecuciones y contadores en `ingestion_runs`, transacciones y rollback.
5. Reconciliación de migraciones UUID con Alembic, pruebas de reejecución y primera ingesta real autorizada.

## 6. Condiciones de aceptación del siguiente hito

- [ ] Integrante ejecuta tests localmente con `.venv-data`.
- [ ] Dry-run real coincide con los conteos del notebook.
- [ ] Se documentan las incidencias sin eliminar registros.
- [ ] El módulo no altera ni `services/api` ni PostgreSQL.
- [ ] Revisión por compañero responsable de datos/ingesta antes del PR.

**Conclusión:** la exploración inicial está completada; el normalizador local se entrega para verificación. La Fase 3 completa sigue abierta.

## 7. Validación en entorno local — 22/10/2026

**Entorno:** Windows, Git Bash, Visual Studio Code y Python mediante `.venv-data`.

**Rama:** `feature/ingesta-eventos-p0`.

### Resultados confirmados

- Se ejecutaron correctamente 8 de 8 pruebas unitarias.
- Se procesó el archivo XLSX original del IGP.
- Se analizaron 25.799 registros sísmicos.
- Se normalizaron correctamente los 25.799 registros.
- No se encontraron registros inválidos.
- Se generaron 25.799 huellas SHA-256 diferentes.
- Se confirmaron 556 registros de 2024.
- Se verificó la coincidencia del SHA-256 del archivo original.
- Se generó un informe JSON mediante `dry-run`.
- No se realizaron conexiones ni escrituras en Supabase.

### Limitaciones

La ejecución no prueba todavía la persistencia en PostgreSQL ni la idempotencia de las inserciones.

Las huellas identifican versiones exactas de registros, pero no sustituyen un identificador oficial de evento sísmico.

La Fase 3 permanece en desarrollo.

**Resultado del hito:** normalizador IGP y simulación local validados satisfactoriamente.
