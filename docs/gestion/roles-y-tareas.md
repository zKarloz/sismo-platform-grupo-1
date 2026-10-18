# Equipo de trabajo — Roles, responsabilidades y entregables

**Proyecto:** Sismo Platform
**Equipo:** 5 integrantes
**Horizonte:** 2 semanas académicas
**Exposiciones:** final de semana 1 (avance), final de semana 2 (entrega final)
**Estado:** Propuesta de asignación, pendiente de aprobación grupal

## 1. Roles y propiedad principal

| Integrante | Rol                                       | Entregable principal                                                                                                                            | Evidencia de aceptación                                                                       |
| ---------- | ----------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| 1          | Líder técnico / DevOps / integración      | CI/CD, configuración Vercel y Render, coordinación de PR, documentación transversal, integración de alertas/reporte básico si alcanza el tiempo | PR revisados; CI aprobado; despliegue funcional; documentación de fases                       |
| 2          | Frontend / UX                             | Diseño de dashboard conectado a API, tabla de eventos, filtros, mapa, gráficos, accesibilidad y responsive                                      | Navegación, estados loading/error/vacío, fuente y fecha visibles, lint/build aprobados        |
| 3          | Backend / API                             | Endpoints FastAPI `/api/v1/events`, detalle, resumen para dashboard, GeoJSON y validaciones; integrar acceso a datos creado por integrante 4    | OpenAPI actualizado; pruebas API; errores y filtros definidos                                 |
| 4          | Ingeniería de datos / Supabase PostgreSQL | Proyecto Supabase, esquema, migraciones, fuentes de eventos, ingesta normalizada, deduplicación y procedencia                                   | Migraciones versionadas; datos reales con fuente; sincronización sin duplicados               |
| 5          | Machine Learning / calidad y pruebas      | Limpieza y versión de dataset, experimento supervisado reproducible, evaluación (métricas), pruebas integradas y límites del modelo             | Dataset versionado; baseline, métricas, validación sin fuga de datos; reporte de limitaciones |

**Regla transversal:** todos documentan lo que construyen, incluyen comentarios por bloques en archivos de código, añaden pruebas y participan en ambas exposiciones. Las tareas críticas se revisan entre al menos dos integrantes.

## 2. Secuencia propuesta, sujeta al cierre de la Fase 0

| Período         | Responsable principal | Trabajo                                                                                           | Dependencia                    |
| --------------- | --------------------- | ------------------------------------------------------------------------------------------------- | ------------------------------ |
| Inicio semana 1 | 1 + todos             | Cerrar Fase 0: alcance, fuente de datos, licencias, campos y backlog. Compartir convenciones Git. | Ninguna                        |
| Semana 1        | 4                     | Supabase, diagrama ER y migraciones iniciales; prueba de ingesta desde fuente verificada.         | Fuente aprobada                |
| Semana 1        | 3                     | Contrato API de eventos, validaciones, paginación, resumen y salud.                               | Esquema acordado con 4         |
| Semana 1        | 2                     | Vista de eventos, dashboard inicial, mapa y estados de conexión.                                  | Contrato API acordado con 3    |
| Semana 1        | 5                     | Estudio de calidad de la fuente, propuesta de variable objetivo ML; preparar pruebas.             | Datos disponibles de 4         |
| Fin semana 1    | 1 + todos             | Integración, CI, despliegue de avance y ensayo de exposición.                                     | PR revisados                   |
| Semana 2        | 4 + 3                 | Robustecer ingesta, filtros y trazabilidad de eventos.                                            | Avance integrado               |
| Semana 2        | 5                     | Dataset, entrenamiento sencillo, evaluación y conclusiones científicamente correctas.             | Datos limpios                  |
| Semana 2        | 2                     | Integrar gráficos estadísticos, detalle, resultados experimentales y alertas de demostración.     | Endpoints disponibles          |
| Semana 2        | 1 + 3                 | Reglas de alertas de demostración, reporte simple, revisión de permisos mínimos según alcance.    | Eventos observados disponibles |
| Fin semana 2    | Todos                 | Pruebas, correcciones, documentación por fase, demo final y exposición.                           | Código integrado               |

**Nota:** las fases del documento original tienen una duración superior a dos semanas. El calendario anterior es una **adaptación académica reducida** que mantiene su orden lógico; no equivale a un MVP empresarial completo.

## 3. Ramas y Pull Requests

- `main`: producción; Render y Vercel despliegan desde esta rama.
- `develop`: integración; es la rama predeterminada en GitHub.
- Ramas sugeridas:
  - `feature/frontend-eventos` (integrante 2)
  - `feature/api-eventos` (integrante 3)
  - `feature/supabase-ingesta` (integrante 4)
  - `feature/ml-experimentos` (integrante 5)
  - `feature/integracion-alertas` (integrante 1, **después** de cerrar la Fase 0 y confirmar dependencias)
- Flujo: actualizar `develop` → crear rama → cambios y pruebas → PR contra `develop` → revisión/CI → merge → PR de `develop` contra `main` únicamente cuando se apruebe una entrega estable.
- No guardar secretos en el repositorio. Configurar variables de entorno en Render/Vercel y copiar `.env.example` en cada máquina.

## 4. Criterios de aceptación mínimos por PR

- [ ] Funcionalidad alineada con la fase y ticket asignado.
- [ ] Comentarios por bloques en el código donde correspondan.
- [ ] Pruebas nuevas o justificación técnica de no necesitarlas.
- [ ] `npm run lint` / `npm run build` o pruebas Python aplicables.
- [ ] No hay secretos, tokens ni claves en el diff.
- [ ] Se actualiza documentación Markdown de la fase afectada.
- [ ] El PR especifica cómo verificar el cambio y sus dependencias.

## 5. Coordinación y bloqueos

- Reunión breve diaria (10–15 minutos): completado, siguiente paso, impedimentos.
- El integrante 4 debe acordar esquema y contrato de datos con el 3 antes de implementar relaciones definitivas.
- El integrante 2 usa respuestas tipadas y estados de carga/error; no inventa datos sísmicos.
- El integrante 5 no presenta un experimento como predicción fiable de terremotos ni como alerta oficial.
- El integrante 1 resuelve conflictos de integración y valida CI/CD antes de cada exposición.
