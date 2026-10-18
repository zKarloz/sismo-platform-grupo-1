# Fase 0 — Guía para revisar el entregable pendiente

**Estado:** ABIERTA — lista de verificación para la próxima revisión del equipo
**Fuente:** PDF `Plan_Desarrollo_Sistema_Monitoreo_Sismico_ML.pdf`, sección 9, Fase 0; secciones 2, 3, 15 y 17.

## Entregable exigido por el PDF

**Documento de alcance, riesgos, fuentes elegidas, casos de uso y backlog priorizado.**

La Fase 0 solicita además definir usuarios y zona inicial, revisar licencia y condiciones de uso, frecuencia y volumen de datos, política de alertas, criterios de aceptación y significado de indicadores (validación con especialista si es posible).

## Decisiones que ya se conocen

- Horizonte académico: dos semanas; exposición de avance al final de la primera y final al término de la segunda.
- 5 integrantes con roles propuestos.
- Stack y despliegue validados: React/Vite/Tailwind en Vercel; FastAPI/Docker en Render; Supabase PostgreSQL previsto.
- GitHub: `main` producción, `develop` integración, `feature/*` colaboración.
- Límite científico: no prometer que ML predice fecha, hora, lugar y magnitud de un terremoto.

## Pendientes de la Fase 0 — por completar antes de empezar la ingesta

- [ ] **Cobertura geográfica:** confirmar si Perú será la zona inicial y qué períodos históricos se analizarán.
- [ ] **Usuarios y casos de uso:** definir perfiles internos, flujos y permisos mínimos.
- [ ] **Fuente elegida:** comparar fuente(s) oficiales/públicas, documentación, disponibilidad de API, fiabilidad y licencias; registrar decisión.
- [ ] **Esquema de campos:** confirmar IDs, UTC, ubicación, magnitud, profundidad, fuente y URL de procedencia.
- [ ] **Frecuencia y volumen:** límites de solicitudes, periodicidad, tamaño esperado y estrategia de recuperación de fallos.
- [ ] **Política de alertas:** distinguir eventos observados, avisos de demostración, estimaciones ML y comunicados oficiales.
- [ ] **Criterios de aceptación:** acordar mínimos medibles para las dos exposiciones.
- [ ] **Backlog priorizado:** P0 imprescindibles; P1 deseables; P2 pospuestos, con responsable y esfuerzo estimado.
- [ ] **Registro de riesgos:** disponibilidad y calidad de fuentes, latencia de Render, conectividad Supabase, limitaciones ML, integración y plazo.
- [ ] **Validación de indicadores:** documentar las limitaciones y quién las revisó; si no hay especialista disponible, dejarlo como limitación explícita.

## Estructura sugerida del entregable de Fase 0

1. Objetivo, contexto y límites científicos.
2. Alcance del prototipo de dos semanas; explícitamente fuera de alcance.
3. Usuarios y casos de uso (mínimo 3–5).
4. Fuente elegida, condiciones de uso, endpoints/campos y política de actualización.
5. Riesgos con probabilidad, impacto y medidas de mitigación.
6. Backlog priorizado, responsables, dependencias y criterios de aceptación.
7. Plan de exposiciones: evidencia del avance (semana 1) y entrega final (semana 2).
8. Registro de decisiones, aprobadores y fecha de cierre.

> Esta guía **no reemplaza ni cierra** `docs/fases/fase-00-alcance.md`. Úsenla como lista de comprobación al revisar y completar el documento oficial.
