# Fase 0 — Descubrimiento y viabilidad

**Estado:** Pendiente de cierre.  
**Responsables:** Integrante 1 (coordinación), integrantes 2–5 (validación).  
**Horizonte:** dos semanas para el prototipo académico; primera exposición al final de la semana 1.

## Objetivo

Acordar alcance reducido, responsabilidades, fuente de datos, límites científicos y criterios de aceptación. Se conserva el orden de fases del PDF de planificación, ajustando el alcance a la duración académica.

## Alcance mínimo propuesto

- Datos de **eventos observados** provenientes de una fuente verificable.
- API para consultar registros con trazabilidad.
- Dashboard, tabla de eventos y mapa, con fuente y fecha.
- Experimento de ML simple y reproducible **etiquetado como experimental**.
- Alertas operativas de demostración basadas en registros recibidos (no alertas oficiales).

## Decisiones tomadas

- Monorepo `sismo-platform`.
- Frontend React + TypeScript + Vite, despliegue previsto en Vercel.
- Backend Python + FastAPI, despliegue previsto en Render con Docker.
- PostgreSQL en Supabase, administrado por el integrante 4.
- GitHub con ramas `main`, `develop` y `feature/*`.

## Decisiones pendientes

- [ ] Elegir y comprobar términos de uso de la fuente sísmica (IGP/alternativa verificable).
- [ ] Confirmar los datos y campos que realmente ofrece la fuente.
- [ ] Delimitar las funciones mínimas demostrables en ambas exposiciones.
- [ ] Definir criterios de evaluación del experimento de ML.
- [ ] Confirmar responsables, plazos y evidencias de exposición.

## Restricción científica y operativa

No afirmar predicción exacta de terremotos. No emitir mensajes atribuidos a entidades oficiales sin integración/validación. Diferenciar observaciones, estimaciones y simulaciones.

**Cierre de fase:** solo cuando se resuelvan y documenten los puntos pendientes.
