# Plan de trabajo y backlog — MVP académico de Sismo Platform

**Proyecto:** Sismo Platform  
**Equipo:** 5 integrantes  
**Duración:** 2 semanas académicas  
**Exposiciones:** final de semana 1 (avance) y final de semana 2 (entrega final)  
**Referencia de alcance:** `docs/fases/fase-00-alcance.md`, sección 11.  
**Estado:** Plan propuesto; los integrantes deben confirmar su asignación.

> **Documento único de gestión:** sustituye a `docs/gestion/roles-y-tareas.md` y a la versión anterior de `docs/gestion/backlog-mvp.md`. Aquí se mantienen roles, cronograma, tareas, responsables, prioridades, dependencias, reglas Git y criterios de aceptación.

## 1. Alcance y criterios de prioridad

El MVP académico se desarrolla siguiendo el orden lógico de las fases del plan técnico original, pero **no equivale a un MVP empresarial completo**. Las funcionalidades que no quepan en el plazo deberán quedar registradas como limitaciones o trabajo futuro.

- **P0 — Imprescindible:** datos sísmicos verificables, persistencia, API de eventos y dashboard/mapa inicial para la primera exposición.
- **P1 — Entrega final:** estadística, calidad de datos, ML didáctico, avisos internos DEMO, reportes básicos y pruebas.
- **P2 — Fuera del alcance de estas dos semanas:** identidad empresarial completa/MFA, notificaciones reales y alta disponibilidad con recuperación probada.
- **Criterio general de finalización (Definition of Done):** PR contra `develop`, revisión, CI exitoso, pruebas aplicables, evidencia manual, comentarios por bloques en código y documentación Markdown actualizada.

## 2. Roles, responsabilidades y evidencias

| Integrante | Rol                                       | Responsabilidades principales                                                                                                                               | Evidencia de aceptación                                                                      |
| ---------- | ----------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| **1**      | Líder técnico / DevOps / integración      | CI/CD, Vercel y Render, coordinación y revisión de PR, integración, documentación transversal; avisos DEMO y reporte básico si las dependencias lo permiten | PR aprobados, CI correcto, versión desplegada y documentos de fase actualizados              |
| **2**      | Frontend / UX                             | Dashboard conectado a API, tabla y filtros, mapa, gráficos, vista de resultados experimentales, accesibilidad y responsive                                  | Datos reales visibles con fuente/fecha, estados de carga/error/vacío, lint y build aprobados |
| **3**      | Backend / API                             | FastAPI: lista y detalle de eventos, filtros, paginación, resumen, GeoJSON, validaciones, reportes y reglas básicas; integración con datos del integrante 4 | OpenAPI, respuestas consistentes, pruebas de endpoints y control de errores                  |
| **4**      | Ingeniería de datos / Supabase PostgreSQL | Proyecto Supabase, esquema relacional, migraciones, fuente(s), ingesta normalizada, trazabilidad y deduplicación                                            | Migraciones versionadas, registros reales con procedencia, sincronizaciones sin duplicados   |
| **5**      | Machine Learning / QA                     | Calidad y versionado del dataset, regresión y clasificación didácticas, baseline, evaluación, pruebas integradas y limitaciones                             | Dataset/versiones, métricas reproducibles, evaluación sin fuga de datos y reporte técnico    |

**Reglas compartidas:** todos participan en ambas exposiciones, comentan el código por bloques, incluyen pruebas y documentan el cierre de cada fase. Las tareas críticas deben tener al menos una segunda revisión.

## 3. Backlog priorizado para GitHub Issues

Los números US son identificadores de planificación; los tickets se crearán como GitHub Issues y se asignarán después de la aprobación grupal.

| Issue                                         | Prioridad | Responsable | Dependencia                         | Entregable / criterio de aceptación                                                               |
| --------------------------------------------- | --------- | ----------- | ----------------------------------- | ------------------------------------------------------------------------------------------------- |
| **US-01 Esquema PostgreSQL**                  | P0        | 4           | Catálogo IGP identificado           | Migraciones, tablas, índices básicos y conexión segura a Supabase                                 |
| **US-02 Ingesta IGP/USGS**                    | P0        | 4           | US-01                               | Fuente identificada, fechas UTC, deduplicación y registro de ejecuciones                          |
| **US-03 API de eventos**                      | P0        | 3           | US-01                               | Lista, detalle, filtros, paginación, OpenAPI y pruebas                                            |
| **US-04 API dashboard/GeoJSON**               | P0        | 3           | US-03                               | KPIs y GeoJSON con filtros coherentes                                                             |
| **US-05 Tabla y filtros**                     | P0        | 2           | US-03                               | Tabla consumiendo FastAPI, estados vacío/error y procedencia                                      |
| **US-06 Dashboard/mapa**                      | P0        | 2           | US-04                               | Indicadores y mapa con puntos de eventos verificados                                              |
| **US-07 Integración/CI/CD**                   | P0        | 1           | Integración de los PR               | Validación de integración, `main` estable y servicios HTTPS; base técnica ya desplegada en Fase 1 |
| **US-08 Calidad del dataset**                 | P0        | 5 + 4       | US-02                               | Nulos, duplicados, versión e informe reproducible                                                 |
| **US-09 Estadísticas**                        | P1        | 2 + 3       | US-04                               | Serie temporal, histograma y dispersión                                                           |
| **US-10 Modelos ML didácticos**               | P1        | 5           | US-08                               | Regresión simple y múltiple, clasificación, baseline y métricas                                   |
| **US-11 Vista experimental**                  | P1        | 2 + 5       | US-10                               | Métricas visibles y advertencia de carácter experimental                                          |
| **US-12 Avisos internos DEMO**                | P1        | 1 + 3       | US-02                               | Reglas por eventos ya observados, registro y etiqueta DEMO                                        |
| **US-13 Exportación CSV**                     | P1        | 3 + 2       | US-03                               | Exportación con filtros, fechas y fuente                                                          |
| **US-14 Permisos/logs mínimos**               | P1        | 1 + 3       | US-03                               | Escrituras protegidas y ausencia de secretos en logs                                              |
| **US-15 QA y documentación final**            | P1        | 5 + todos   | US-01 a US-14 que entren en alcance | Pruebas, informe, guion de demo y documentación de fases                                          |
| **US-16 Identidad empresarial/MFA**           | P2        | 1 + 3       | Futuro                              | Fuera del compromiso académico                                                                    |
| **US-17 Notificaciones reales**               | P2        | 1 + 3       | Futuro                              | Fuera del compromiso académico                                                                    |
| **US-18 Alta disponibilidad/backup ensayado** | P2        | 1 + 4       | Futuro                              | Fuera del compromiso académico                                                                    |

## 4. Cronograma y entregables por semana

| Período             | Responsable | Tareas principales                                                               | Dependencia             |
| ------------------- | ----------- | -------------------------------------------------------------------------------- | ----------------------- |
| **Inicio semana 1** | 1 + todos   | Ratificar cierre de Fase 0, fuente(s), campos, licencias, backlog y normas Git   | Aprobación de alcance   |
| **Semana 1**        | 4           | Supabase, diagrama ER, migraciones iniciales y primera ingesta verificable       | Fuente aprobada         |
| **Semana 1**        | 3           | Contrato de API, eventos, filtros, resumen y GeoJSON                             | Esquema acordado con 4  |
| **Semana 1**        | 2           | Tabla, dashboard/mapa básicos y estados de interfaz                              | Contrato acordado con 3 |
| **Semana 1**        | 5           | Perfil de calidad, propuesta de variable objetivo de ML y preparación de pruebas | Datos del 4             |
| **Fin semana 1**    | 1 + todos   | Integración de PR, CI, despliegue estable y ensayo de exposición                 | Funciones P0 listas     |
| **Semana 2**        | 3 + 4       | Robustecer API e ingesta, filtros, deduplicación y trazabilidad                  | Avance integrado        |
| **Semana 2**        | 5           | Dataset, modelos sencillos, evaluación, advertencias y pruebas                   | Datos limpios           |
| **Semana 2**        | 2           | Gráficos, detalles, resultados ML y visualización de avisos DEMO                 | Endpoints disponibles   |
| **Semana 2**        | 1 + 3       | Avisos internos DEMO, exportación básica, permisos y logs mínimos                | Eventos observados      |
| **Fin semana 2**    | Todos       | Correcciones, pruebas, documentación, demostración y exposición final            | Funciones integradas    |

### Resumen individual de entregables

| Integrante | Primera exposición                                        | Segunda exposición                                         |
| ---------- | --------------------------------------------------------- | ---------------------------------------------------------- |
| **1**      | Coordinación, contratos, PR, CI/CD y despliegue de avance | Avisos DEMO, integración transversal y documentación final |
| **2**      | Tabla de eventos, KPI y mapa mínimo                       | Gráficos, estados y vista experimental de ML               |
| **3**      | Eventos, detalle, dashboard y GeoJSON                     | Permisos mínimos, avisos DEMO, exportación y pruebas       |
| **4**      | Migraciones, catálogo y primera ingesta                   | Controles de calidad, duplicados y documentación de datos  |
| **5**      | Revisión de dataset y plan de pruebas                     | Regresión, clasificación, métricas y pruebas integradas    |

## 5. Convenciones de Git y Pull Requests

- **`main`:** rama estable; producción de Render y Vercel.
- **`develop`:** rama predeterminada de GitHub y destino para integración.
- **Ramas sugeridas:**
  - Integrante 1: `feature/avisos-demo` (una vez disponibles los eventos y el alcance).
  - Integrante 2: `feature/eventos-frontend`.
  - Integrante 3: `feature/api-eventos`.
  - Integrante 4: `feature/supabase-ingesta`.
  - Integrante 5: `feature/ml-experimentos`.
- **Flujo:** actualizar `develop` → crear rama → implementar/probar → abrir PR contra `develop` → revisar CI y código → merge → llevar `develop` a `main` mediante PR para cada entrega estable.
- **Seguridad:** no subir secretos ni archivos `.env`; configurar credenciales en los entornos correspondientes. Evitar ediciones simultáneas de archivos comunes sin coordinación.

### Lista de aceptación por Pull Request

- [ ] Ticket e identificación de fase correctos.
- [ ] Código con comentarios por bloques donde corresponde.
- [ ] Pruebas añadidas o ausencia justificada.
- [ ] `npm run lint` y `npm run build` o pruebas Python aplicables.
- [ ] CI exitoso.
- [ ] No se agregan credenciales, tokens ni datos sensibles.
- [ ] Markdown de la fase actualizado.
- [ ] El PR indica cómo verificar su funcionamiento y sus dependencias.

## 6. Coordinación y gestión de bloqueos

- Reunión de 10–15 minutos al día: avances, siguiente tarea y bloqueos.
- Integrantes **3 y 4:** pactar esquema y contrato de eventos antes de fijar tablas/endpoints definitivos.
- Integrante **2:** consumir respuestas tipadas de API, mostrar estados de carga/error y no inventar sismos.
- Integrante **5:** no afirmar que modelos experimentales predicen cuándo ocurrirá un terremoto; registrar métricas, limitaciones y fuga de datos.
- Integrante **1:** verificar integración, CI y despliegues antes de cada exposición.
- Si una dependencia impide completar una tarea P1, priorizar las P0 y documentar el recorte del alcance.

## 7. Hitos y criterios de demostración

**Primera exposición:** registros sísmicos reales persistidos con fuente y fecha, API consumible, tabla, dashboard/mapa inicial, CI y demostración funcional.

**Exposición final:** estadísticas, calidad y versionado del dataset, experimentos ML evaluados y etiquetados, avisos internos de demostración, pruebas y documentación.

**Límite científico:** las estimaciones experimentales, la clasificación de eventos registrados y los avisos internos no equivalen a predicciones fiables de terremotos ni a alertas oficiales de IGP/INDECI.
