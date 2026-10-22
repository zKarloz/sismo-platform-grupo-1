-- =====================================================
-- PROPUESTA FASE 03 - NO EJECUTAR SIN AUTORIZACION.
-- Esquema de referencia: database_tables_definition_2110_2.txt
-- PostgreSQL/Supabase con PK UUID y cinco FK.
-- No reemplaza la migracion inicial ni Alembic.
-- =====================================================

-- =====================================================
-- BLOQUE 1: Inspecciones previas (SOLO LECTURA).
-- Antes de aprobar, consultar metadatos y posibles
-- inconsistencias de cualquier columna preexistente.
-- =====================================================
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name = 'seismic_events'
  AND column_name IN ('source_id', 'external_id', 'record_fingerprint')
ORDER BY column_name;

SELECT indexname, indexdef
FROM pg_indexes
WHERE schemaname = 'public'
  AND tablename = 'seismic_events'
ORDER BY indexname;

-- =====================================================
-- BLOQUE 2: CAMBIOS PROPUESTOS, COMENTADOS.
-- Deben ejecutarse SOLO tras aprobacion del equipo,
-- copia de seguridad, verificacion de columnas reales,
-- reconciliacion Alembic y revision del responsable BD.
-- NO quitar comentarios en este archivo por ahora.
-- =====================================================

-- BEGIN;
--
-- ALTER TABLE public.seismic_events
--     ADD COLUMN IF NOT EXISTS record_fingerprint text;
--
-- COMMENT ON COLUMN public.seismic_events.record_fingerprint IS
--     'SHA-256 hex lowercase de parametros exactos del registro IGP v1; no es ID oficial ni identidad fisica estable.';
--
-- ALTER TABLE public.seismic_events
--     ADD CONSTRAINT ck_seismic_events_record_fingerprint_format
--     CHECK (
--         record_fingerprint IS NULL
--         OR record_fingerprint ~ '^[0-9a-f]{64}$'
--     );
--
-- ALTER TABLE public.seismic_events
--     ADD CONSTRAINT ck_seismic_events_fingerprint_requires_source
--     CHECK (record_fingerprint IS NULL OR source_id IS NOT NULL);
--
-- -- La condicion WHERE importa: se admiten filas antiguas
-- -- con huella NULL y no se restringen otros proveedores.
-- CREATE UNIQUE INDEX uq_seismic_events_source_record_fingerprint
--     ON public.seismic_events (source_id, record_fingerprint)
--     WHERE source_id IS NOT NULL AND record_fingerprint IS NOT NULL;
--
-- COMMIT;

-- =====================================================
-- BLOQUE 3: Patron SQL ilustrativo del futuro writer.
-- No se usa aqui, porque faltan rol RLS y transacciones.
-- INSERT ... ON CONFLICT debe inferir el indice parcial
-- usando la misma condicion WHERE del indice.
-- =====================================================
-- INSERT INTO public.seismic_events
--     (source_id, record_fingerprint, external_id, occurred_at,
--      latitude, longitude, magnitude, magnitude_type, depth_km,
--      place, source_url, review_status)
-- VALUES
--     (:source_id, :record_fingerprint, NULL, :occurred_at,
--      :latitude, :longitude, :magnitude, :magnitude_type, :depth_km,
--      :place, :source_url, 'pending')
-- ON CONFLICT (source_id, record_fingerprint)
--     WHERE source_id IS NOT NULL AND record_fingerprint IS NOT NULL
-- DO NOTHING
-- RETURNING id;

-- =====================================================
-- BLOQUE 4: No otorgar permisos aqui.
-- Rol de escritura/RLS se definira aparte.
-- Tampoco se aplica sobre Supabase en esta etapa.
-- =====================================================
