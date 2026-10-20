# Fase 0 — Descubrimiento y viabilidad

> **Proyecto:** Sismo Platform — Sistema de monitoreo sísmico, analítica y alertas responsables
> **Documento:** Entregable formal de Fase 0, según sección 9 del plan técnico (PDF, versión 1.0 de octubre de 2026).
> **Estado de planificación:** CERRADA — propuesta consolidada por el integrante 1; **pendiente de ratificación por los cinco integrantes**.
> **Fecha de preparación:** 19/10/2026
> **Duración académica:** dos semanas, cinco integrantes, exposición de avance al finalizar la semana 1 y exposición final al finalizar la semana 2.
> **Alcance del cierre:** decisiones de viabilidad, selección de fuentes, casos de uso, riesgos, backlog y aceptación; no equivale a tener desarrollados los módulos.

## 1. Fundamento y objetivo

La sección 9 del PDF exige como entregable de Fase 0 un **documento de alcance, riesgos, fuentes elegidas, casos de uso y backlog priorizado**. Pide definir usuarios, cobertura, fuente y condiciones de uso, frecuencia y volumen, política de alertas y criterios de aceptación. La propuesta sigue las secciones 1–3, 9, 10, 14, 15 y 17 del PDF y reduce las funcionalidades empresariales para un prototipo académico de dos semanas.

**Objetivo:** visualizar y consultar sismos **ya observados y reportados**, conservar su procedencia, explorar sus patrones históricos y mostrar ejercicios supervisados de Machine Learning claramente identificados como experimentales. No se afirma poder anticipar con certeza fecha, lugar y magnitud de futuros terremotos.

## 2. Decisiones aprobadas para la arquitectura académica

| Decisión             | Definición                                                                                                                              | Responsable |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------- | ----------- |
| Repositorio          | Monorepo `sismo-platform`, `develop` integración y `main` producción                                                                    | 1           |
| Interfaz             | React, TypeScript, Vite, Tailwind CSS y `lucide-react`; tema claro predeterminado y oscuro opcional                                     | 2           |
| Backend              | Python, FastAPI, Pydantic, SQLAlchemy y API REST `/api/v1`                                                                              | 3           |
| Persistencia         | PostgreSQL administrado en Supabase; migraciones versionadas con Alembic                                                                | 4           |
| Datos y experimentos | pandas, NumPy, scikit-learn, joblib, validación temporal y métricas                                                                     | 5           |
| Despliegue           | Vercel (frontend) y Render/Docker (backend), por `main` y HTTPS                                                                         | 1           |
| Cobertura inicial    | Perú y costa adyacente para consultas, con etiquetas de cobertura y proveedor; la ventana rectangular NO equivale al límite territorial | 3–4         |
| Usuarios iniciales   | Equipo académico: administrador/coordinador, analista, operador de demostración y lector                                                | 1–3         |
| Públicos/terceros    | Lectura y demostración; nunca operación oficial de protección civil                                                                     | Todos       |

Los endpoints públicos y el sitio ya desplegados se documentan en `docs/fases/fase-01-cierre.md`.

## 3. Fuentes elegidas y condiciones de utilización

### Matriz comparativa de fuentes y condiciones de uso

La siguiente matriz concentra las decisiones de fuente, licencia, formato y estado de integración. Los apartados posteriores detallan las condiciones de cada proveedor.

| Fuente                  | Tipo                      | Cobertura/uso                           | Formato/acceso                  | Licencia/condición                                                                                             | Estado                            |
| ----------------------- | ------------------------- | --------------------------------------- | ------------------------------- | -------------------------------------------------------------------------------------------------------------- | --------------------------------- |
| IGP, catálogo nacional  | Primaria histórica        | Perú, 1960–2025                         | CSV, diccionario y metadatos    | **Open Data Commons Attribution License**, ficha de la PNDA consultada en 2026; conservar atribución y versión | Identificada; importar en Fase 3  |
| IGP CENSIS              | Referencia de actualidad  | Sismos reportados oficialmente por IGP  | Reportes web y consulta pública | API de ingesta masiva y permisos para automatización **no verificados**                                        | Solo consulta/enlace; no scraping |
| USGS Earthquake Catalog | Complementaria de ingesta | Eventos recientes, zona Perú/adyacentes | API GET, GeoJSON/CSV y filtros  | USGS: información generalmente de dominio público en EE. UU.; citar y revisar excepciones                      | API documentada; prueba en Fase 3 |
| INDECI/COEN             | Referencia institucional  | Prevención y avisos oficiales           | Boletines, comunicados, normas  | No asumir permiso de publicación o emisión de alertas en nombre de INDECI                                      | Enlazar, no suplantar alertas     |

### 3.1 IGP — Catálogo sísmico histórico (fuente primaria para analítica)

- **Entidad:** Instituto Geofísico del Perú (IGP), mediante el catálogo de la Plataforma Nacional de Datos Abiertos.
- **Repositorio:** https://www.datosabiertos.gob.pe/dataset/cat%C3%A1logo-s%C3%ADsmico-desde-1960-instituto-geof%C3%ADsico-del-per%C3%BA-igp
- **Cobertura documentada de la versión consultada:** 1960–2025; disponibilidad de CSV, metadatos y diccionario de datos.
- **Licencia indicada en la ficha vigente consultada el 19/10/2026:** Open Data Commons Attribution License (ODC-BY). Conservar atribución, enlaces, versión/fecha y cualquier aviso de licencia aplicable. La ficha histórica del portal tuvo revisiones sin licencia indicada; conservar evidencia de la versión usada y comprobar metadatos antes de publicar redistribuciones.
- **Actualización declarada en la ficha:** anual, **no** flujo en tiempo real.
- **Uso permitido previsto:** carga inicial verificable a PostgreSQL, series temporales, mapas, filtros y experimentos ML sobre registros históricos.
- **Estado:** fuente y licencia identificadas; **descarga técnica, verificación del archivo, tamaño real y mapeo del diccionario son pruebas de entrada para Fase 3**. No declarar la importación terminada en Fase 0.

### 3.2 IGP — Centro Sismológico Nacional, CENSIS (referencia oficial de eventos recientes)

- **Sitio oficial:** https://censis.igp.gob.pe/
- **Uso:** comparar reportes recientes, mostrar enlaces a reportes oficiales y comprobar parámetros (fecha, localización, magnitud y profundidad).
- **No verificado:** documentación de una API pública de ingesta periódica, condiciones de automatización y límites técnicos. **No programar scraping del sitio ni inventar endpoints.** Si existe integración autorizada, el integrante 4 registrará URL, licencia, frecuencia y contrato antes de incorporarla.

### 3.3 USGS — Earthquake Catalog API (fuente complementaria de ingesta automatizada)

- **Documentación:** https://earthquake.usgs.gov/fdsnws/event/1/
- **Formato propuesto:** GeoJSON vía `GET /fdsnws/event/1/query` con `format=geojson`, límites temporales, magnitud, profundidad y coordenadas; respuesta incluye ID del proveedor y URL de origen.
- **Uso:** consultas automatizadas de eventos recientes en una zona aproximada del Perú, con registro **expreso** del proveedor `USGS`, sin identificarlos como reportes CENSIS.
- **Derechos:** la política de USGS considera sus datos producidos por la entidad generalmente de dominio público en EE. UU.; se dará crédito a la fuente y se revisarán advertencias específicas del conjunto de datos.
- **Condición:** probar una consulta real de API, límites, fallas y zona geográfica en Fase 3. El alcance puede variar respecto de la cobertura del IGP.

### 3.4 INDECI — información preventiva y comunicaciones oficiales

- **Sitio:** https://portal.indeci.gob.pe/
- **Referencia de protocolos:** https://www.gob.pe/institucion/indeci/normas-legales/5412520-031-2024-indeci (directiva para empleo de SISMATE por INDECI).
- **Uso:** enlace y contexto preventivo; NO emisión de boletines, alertas públicas ni notificaciones como si provinieran de INDECI, SASPe o SISMATE.
- **Regla:** una alerta interna del prototipo basada en una regla de magnitud se denomina **«aviso interno de demostración por evento reportado»**, conserva fuente y hora, y jamás utiliza identidad visual de alarma oficial.

### 3.5 Herramientas técnicas de referencia del PDF

- FastAPI: https://fastapi.tiangolo.com/
- React: https://react.dev/
- PostgreSQL: https://www.postgresql.org/docs/
- scikit-learn: https://scikit-learn.org/stable/

### 3.6 Verificaciones técnicas pendientes para la Fase 3

**Estado:** las fuentes y las condiciones previstas se seleccionaron en la Fase 0; las siguientes actividades todavía **no se han ejecutado** y no forman parte de su cierre.

- [ ] Descargar el CSV IGP, registrar nombre de archivo, tamaño, fecha y huella SHA-256.
- [ ] Descargar/leer el diccionario oficial y registrar columnas y nulos.
- [ ] Conservar evidencia de licencia ODC-BY y elaborar atribución visible en interfaz/reportes.
- [ ] Probar una consulta a USGS, registrar URL exacta, respuesta, fecha y manejo de errores.
- [ ] Configurar ventana geográfica orientativa y filtros posconsulta; evitar equipararla con límites políticos.
- [ ] Comparar al menos algunos eventos contra reportes CENSIS sin afirmar que ambas fuentes son equivalentes.
- [ ] Definir paginación, límites, frecuencia efectiva, caché y si el alojamiento permite sincronización periódica.
- [ ] Documentar cualquier permiso o restricción específica si se proyecta consumir CENSIS automáticamente.

**Responsables de la validación de fuentes:** integrante 4 (datos e ingesta), integrante 3 (contrato de API) e integrante 1 (cumplimiento y documentación).

## 4. Cobertura, cadencia y volumen

| Parámetro         | Compromiso académico                                                                                                      | Límite / advertencia                                                                                             |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Cobertura         | Perú y entorno costero; filtros por periodo y coordenadas                                                                 | Un _bounding box_ incluye también zonas de países vecinos/mar; no atribuir automáticamente región administrativa |
| Historia          | Catálogo IGP 1960–2025; dashboard por defecto con periodo reducido                                                        | Se anotará la versión efectiva del CSV y su número de filas después de descargarlo                               |
| Eventos recientes | USGS vía API documentada; referencia cruzada con CENSIS                                                                   | No garantizar igualdad de registros, magnitudes o latencias entre proveedores                                    |
| Carga inicial     | Una importación de CSV por lotes a PostgreSQL                                                                             | Validación de columnas, UTC, duplicados, rangos e identidad de fuente                                            |
| Actualización     | Sincronización manual protegida para exposición; automática cada 60 min **solo si infraestructura y pruebas lo permiten** | No rotular como «tiempo real»; mostrar `last_sync_at`, fecha de origen y estado de fuente                        |
| Consultas         | Paginación y filtros; límite inicial recomendado 100 filas por página y consultas históricas acotadas                     | El integrante 3 definirá límites reales tras pruebas                                                             |
| Volumen           | Catálogo IGP de decenas de miles de registros; el portal muestra una versión de ~24 mil filas                             | El conteo exacto se verificará al importar; no fijar capacidad garantizada                                       |
| Retención         | Eventos históricamente consultados y registro básico de ingesta                                                           | Sin contraseñas ni secretos en tablas, logs, código o repositorio                                                |

## 5. Personas usuarias y casos de uso

| ID    | Actor                    | Caso de uso                                                     | Resultado verificable                                       |
| ----- | ------------------------ | --------------------------------------------------------------- | ----------------------------------------------------------- |
| CU-01 | Lector                   | Consultar sismos por fecha, magnitud y ubicación                | Tabla paginada con datos y fuente                           |
| CU-02 | Lector                   | Ver epicentros en mapa y abrir detalle                          | Coordenadas, magnitud, profundidad, fecha UTC y URL fuente  |
| CU-03 | Analista                 | Revisar conteos, series temporales y distribución de magnitudes | Gráficas con periodo, tamaño de muestra y actualización     |
| CU-04 | Operador de datos        | Importar o sincronizar registros verificables                   | Nuevos registros, duplicados controlados y log de ejecución |
| CU-05 | Analista ML              | Ejecutar experimento simple, múltiple y/o clasificación         | Dataset, baseline, métricas y limitaciones visibles         |
| CU-06 | Operador de demostración | Evaluar regla interna de aviso ante evento recibido             | Etiqueta DEMO, fuente y ausencia de difusión oficial        |
| CU-07 | Administrador            | Consultar salud del sistema y errores de conectores             | Estado, última sincronización y trazabilidad de fallos      |

**Acceso:** lectura demostrativa abierta o interna según alcance; operaciones de sincronización, entrenamiento o cambios de reglas se ejecutarán desde rutas protegidas o herramientas del equipo, nunca mediante un endpoint público sin autenticación. La autenticación completa por roles sigue siendo un alcance reducible en Fase 2.

## 6. Módulos del PDF y alcance comprometido

| Módulo del plan             | Compromiso en 2 semanas                                                           |
| --------------------------- | --------------------------------------------------------------------------------- |
| Dashboard                   | Funcional: KPI y series usando datos persistidos                                  |
| Eventos sísmicos            | Funcional: lista, filtros y detalle con procedencia                               |
| Mapa sísmico                | Funcional: puntos geográficos reales                                              |
| Análisis estadístico        | Básico: series, magnitudes y magnitud vs. profundidad                             |
| Preparación de datos        | Básico: nulos, duplicados, reglas documentadas y versión de dataset               |
| Modelos ML                  | Académico: baseline, regresión y clasificación si existen datos suficientes       |
| Estimaciones experimentales | Opcional: visualización separada y etiquetada; nunca alerta oficial               |
| Reglas de alertas           | Demostración interna, sin envío externo                                           |
| Centro de alertas           | Historial simple de avisos de demostración si se completa la regla                |
| Fuentes de datos            | Estado del catálogo IGP, consulta USGS y última sincronización                    |
| Reportes                    | CSV básico, condicionado a pruebas                                                |
| Usuarios y roles            | Roles definidos en diseño; autorización administrativa mínima si alcanza el plazo |
| Auditoría y configuración   | Logs básicos de ingesta y acciones; no auditoría empresarial completa             |

**Fuera de alcance:** predicción exacta de terremotos, alertamiento temprano certificado, uso de SISMATE/SASPe, envío masivo de SMS, sistemas HA/24x7, MFA completo, alta disponibilidad, recuperación garantizada y modelo ML científicamente validado como pronóstico.

## 7. Machine Learning — política científica y definición del experimento

- **Pregunta educativa inicial:** explorar asociaciones entre magnitud, profundidad, coordenadas y periodo de eventos **ya registrados**; medir qué tan bien modelos simples aproximan etiquetas conocidas, no anticipar sismos.
- **Regresión lineal simple:** magnitud observada como variable objetivo y profundidad como variable explicativa; análisis exploratorio, sin causalidad implícita.
- **Regresión múltiple:** magnitud observada frente a profundidad, latitud y longitud, y variables de calendario justificadas y disponibles en cada registro; resultados de laboratorio, no pronóstico de eventos futuros.
- **Clasificación:** categoría de magnitud del evento reportado usando profundidad, ubicación y variables temporales; **no** utilizar magnitud ni derivadas como _features_ de esa misma clase.
- **Evaluación:** comparar contra `DummyRegressor`/`DummyClassifier`, partición cronológica para reducir fuga temporal, fijar semilla, registrar versión y datos; regresión: MAE, RMSE y R²; clasificación: precision, recall, F1 y matriz de confusión.
- **Criterio de honestidad:** si el resultado no supera baseline, se reporta abiertamente. Ninguna salida se llama «probabilidad de terremoto mañana».
- **Validación especializada:** no se cuenta actualmente con revisión de un sismólogo; se declara esta limitación y se buscará asesoría académica si está disponible.

## 8. Política de alertas y comunicación pública

1. **Evento observado:** registro de un proveedor con ID, fecha, fuente y URL de procedencia.
2. **Aviso interno por umbral:** regla configurable de demostración (p. ej., magnitud >= 5.0), disparada DESPUÉS de recibir un registro; no equivale a peligro confirmado ni estima intensidad local.
3. **Estimación experimental:** producto del laboratorio ML separado física y visualmente de eventos/avisos.
4. **Comunicado oficial:** solo enlace o reproducción autorizada con atribución verificable; no inventar ni emitirlo en nombre del IGP/INDECI.
5. No habilitar envíos públicos, notificaciones masivas, campañas o automatizaciones de emergencia en este proyecto académico.
6. El frontend mostrará en vistas pertinentes: **«Prototipo académico de monitoreo. No reemplaza avisos oficiales del IGP o INDECI.»**

### Texto de advertencia obligatorio en la aplicación

> Sismo Platform es un prototipo académico que presenta eventos registrados por fuentes identificadas y experimentos estadísticos. No es un servicio oficial de alerta temprana ni predice con certeza terremotos. Para comunicaciones oficiales, consulta al IGP e INDECI.

La gráfica y la tabla de eventos deben indicar proveedor, fecha/hora de actualización y vínculo de procedencia. La estimación ML nunca se publicará en la misma categoría visual que una alerta oficial.

## 9. Riesgos de viabilidad y mitigación

| ID  | Riesgo                                                     | Prob. / impacto | Mitigación y propietario                                                                              |
| --- | ---------------------------------------------------------- | --------------- | ----------------------------------------------------------------------------------------------------- |
| R01 | IGP no ofrece API documentada para automatización reciente | Alta / Media    | Usar catálogo abierto histórico y USGS API complementaria; no scraping (4)                            |
| R02 | Datos IGP/USGS difieren o tienen huecos                    | Alta / Media    | Mantener IDs por proveedor, no fusionar eventos sin reglas justificadas; procedencia visible (3–4)    |
| R03 | Cambio de licencia/formato de dataset                      | Media / Alta    | Registrar evidencia de ficha, CSV y metadatos, atribuir y revisar antes de redistribuir (4–1)         |
| R04 | Cuotas, suspensión o latencia en Render/Supabase           | Media / Alta    | Verificar salud, reintentos limitados, caché y captura demostrativa de respaldo (1, 4)                |
| R05 | Fuga de credenciales o endpoint de sync abierto            | Media / Alta    | `.env` excluidos de Git, permisos de base de datos, secretos en Render; proteger escrituras (1, 3, 4) |
| R06 | Modelos con fuga de datos o conclusiones engañosas         | Alta / Alta     | Partición temporal, baseline, etiquetas «experimental», revisión de variables (5)                     |
| R07 | Presentar avisos internos como oficiales                   | Media / Crítica | Etiquetas DEMO y separación visual, enlaces oficiales; prohibir difusión pública (1, 2, 5)            |
| R08 | Demoras por trabajo paralelo y 2 semanas                   | Alta / Alta     | P0 limitado, contratos API iniciales, PR pequeños y revisión diaria de bloqueos (todos)               |
| R09 | Pruebas con pocas observaciones                            | Media / Media   | Carga histórica IGP y fallback de ensayo reproducible para demostración; no inventar resultados (4–5) |

## 10. Entregables de las dos exposiciones

### Semana 1 — Primer avance

- Infraestructura React/Vercel + FastAPI/Render probada (Fase 1 existente).
- Supabase conectado, esquema mínimo `data_sources`, `seismic_events`, `ingestion_runs`, migración reproducible.
- Al menos una importación verificable de registros históricos IGP o de USGS, con ID de origen, UTC y sin duplicación ante reejecución.
- API `GET /api/v1/events` (filtros y paginación) y `GET /api/v1/dashboard/summary` básicos.
- Tabla de eventos, dashboard inicial y mapa, o plan B documentado si hay bloqueo real de proveedor.
- Cada integrante explica parte implementada y muestra su PR o evidencia técnica.

### Semana 2 — Entrega final

- Dashboard, mapa, filtros y gráficas reconciliados con API.
- Calidad de dataset registrada (faltantes, duplicados, filas válidas, versión).
- Experimentos de regresión simple/múltiple y clasificación documentados, evaluados y **claramente experimentales**.
- Reglas de aviso interno de demostración, y CSV básico si no compromete funciones P0.
- Pruebas backend/frontend, revisión de seguridad, README, evidencias y documentación Markdown de fases completadas.
- Demostración en `main`, sin depender de una llamada externa inestable durante la presentación (preparar caché/dataset persistido).

## 11. Backlog priorizado y responsables

**P0 = imprescindible para el avance y el final; P1 = objetivo de la segunda semana; P2 = ampliación futura.**

| ID    | Prioridad | Trabajo                                                                             | Responsable | Fase del PDF | Dependencias        |
| ----- | --------- | ----------------------------------------------------------------------------------- | ----------- | ------------ | ------------------- |
| US-01 | P0        | Esquema PostgreSQL, fuente e índices básicos, migraciones                           | 4           | 1 / 3        | Fuente seleccionada |
| US-02 | P0        | Importación IGP CSV o consulta USGS; validaciones, procedencia, deduplicación       | 4           | 3            | US-01               |
| US-03 | P0        | Endpoints lista/detalle de eventos, filtros y paginación                            | 3           | 3            | US-01               |
| US-04 | P0        | Resumen dashboard y GeoJSON, respuestas consistentes                                | 3           | 4            | US-03               |
| US-05 | P0        | Tabla de eventos, detalle y filtros conectados a la API                             | 2           | 4            | US-03               |
| US-06 | P0        | Dashboard con KPIs y mapa básico                                                    | 2           | 4            | US-04               |
| US-07 | P0        | CI, control de ramas, despliegue y soporte de integración                           | 1           | 1 / 9        | Todas               |
| US-08 | P0        | Preparación de datos, auditoría de calidad y pruebas de ingesta                     | 5 + 4       | 5            | US-02               |
| US-09 | P1        | Gráficos temporales, magnitud/profundidad y exportación filtrada                    | 2 + 3       | 4 / 8        | US-04               |
| US-10 | P1        | Regresión simple/múltiple y clasificación con baseline y métricas                   | 5           | 6            | US-08               |
| US-11 | P1        | Vista de resultados experimentales y limitaciones                                   | 2 + 5       | 6            | US-10               |
| US-12 | P1        | Regla de aviso interno de demostración e historial simple                           | 1 + 3       | 7            | US-02               |
| US-13 | P1        | CSV básico y documentación de filtros/fuente                                        | 3 + 2       | 8            | US-03               |
| US-14 | P1        | Revisión de permisos mínimos y logs críticos                                        | 1 + 3       | 2 / 9        | US-03               |
| US-15 | P1        | Pruebas de integración, auditoría de seguridad y demo final                         | 5 + todos   | 9            | US-01 a 14          |
| US-16 | P2        | Login empresarial completo, MFA, administración avanzada de roles                   | 3 + 1       | 2 / 8        | Futuro              |
| US-17 | P2        | Envío SMS/email, colas, reintentos multicanal y aprobación formal                   | 1 + 3       | 7            | Futuro              |
| US-18 | P2        | Infraestructura de alta disponibilidad, backups ensayados y observabilidad integral | 1 + 4       | 9            | Futuro              |

**Control documental:** esta tabla constituye el backlog priorizado de la Fase 0. Las tareas podrán registrarse también como _GitHub Issues_, pero este archivo contiene el alcance y las dependencias aprobados o pendientes de ratificación.

## 12. Criterios de aceptación medibles

- **CA-01:** documentación de fuente y licencia (IGP histórico; USGS programático) accesible y atribuida.
- **CA-02:** todos los eventos expuestos presentan ID de proveedor, URL de fuente, hora UTC, latitud, longitud, magnitud y profundidad (o `null` explícito si falta y el registro cumple la política de calidad).
- **CA-03:** reimportar un conjunto de prueba no duplica `(source_id, external_id)`; `ingestion_runs` registra éxito/error y conteos.
- **CA-04:** tabla, mapa y KPIs coinciden con los mismos filtros y resultados de la API.
- **CA-05:** la API tiene pruebas automatizadas para rutas base, filtros y casos de error; CI aprobado.
- **CA-06:** el ML registra versión del dataset, corte temporal, features, target, baseline y métricas, sin confundirlo con aviso sísmico.
- **CA-07:** avisos internos contienen «DEMO» y procedencia; ningún canal de alerta pública queda habilitado.
- **CA-08:** deploy Vercel/Render funciona por HTTPS con CORS restringido al frontend legítimo.
- **CA-09:** el trabajo de todos los integrantes se encuentra en PR rastreables y cada fase terminada se documenta en Markdown.
- **CA-10:** la presentación final funciona sobre datos persistidos y muestra hora de actualización, periodos y limitaciones.

## 13. Puertas de entrada para desarrollo (no bloquean cierre de planificación)

- **Fase 3 — datos:** integrante 4 descargará y verificará el CSV IGP, licencia/versionado y diccionario, probará la API USGS y documentará el endpoint exacto y sus resultados. No se da por implementada ninguna integración hasta aprobar la prueba.
- **Fase 2 — seguridad:** integrante 3 e integrante 1 decidirán y validarán controles de lectura, acceso administrativo y sincronización; ninguna ruta peligrosa quedará abierta por comodidad.
- **Fase 6 — ML:** integrante 5 validará el significado y disponibilidad real de cada variable y registrará que no existe validación sismológica externa.
- **Fase 9 — operaciones:** integrante 1 comprobará límites del despliegue gratuito y acordará estrategia de demostración segura, sin prometer alta disponibilidad.

## 14. Acta de cierre y ratificación del equipo

**Decisión de coordinación:** se considera **cerrada la planificación de Fase 0** con el alcance, fuentes, riesgos, casos de uso, backlog y criterios consignados. La viabilidad de la API USGS y de importaciones se verificará en implementación, y la integración con CENSIS automatizada no forma parte de este compromiso sin autorización/documentación.

**Ratificación grupal pendiente:** cada integrante debe revisar su responsabilidad y el backlog antes del primer trabajo independiente. Registrar aprobación en un PR hacia `develop`; no afirmar que los cinco ya aprobaron antes de recibir sus revisiones.

| Integrante | Responsabilidad principal                             | Revisión del documento          |
| ---------- | ----------------------------------------------------- | ------------------------------- |
| 1          | Coordinación, DevOps, PR, integración y documentación | Proponente; firma por confirmar |
| 2          | Frontend/UX                                           | Pendiente                       |
| 3          | Backend/API                                           | Pendiente                       |
| 4          | Supabase/datos/ingesta                                | Pendiente                       |
| 5          | ML/QA                                                 | Pendiente                       |

## 15. Referencias verificadas (consulta: 19/10/2026)

1. **PDF del proyecto, versión 1.0, octubre 2026:** secciones 2–5, 9–10, 14–17.
2. **IGP — Catálogo sísmico 1960–2025, licencia ODC-BY y frecuencia anual:** https://www.datosabiertos.gob.pe/dataset/cat%C3%A1logo-s%C3%ADsmico-desde-1960-instituto-geof%C3%ADsico-del-per%C3%BA-igp
3. **IGP — CENSIS:** https://censis.igp.gob.pe/
4. **USGS — FDSN Earthquake Catalog:** https://earthquake.usgs.gov/fdsnws/event/1/
5. **USGS — créditos y derechos:** https://www.usgs.gov/information-policies-and-instructions/copyrights-and-credits
6. **USGS — formato y catálogos GeoJSON:** https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php
7. **INDECI — directiva SISMATE:** https://www.gob.pe/institucion/indeci/normas-legales/5412520-031-2024-indeci
8. **INDECI — comunicación de SASPe/SISMATE:** https://www.gob.pe/institucion/indeci/noticias/1263515-indeci-anuncia-activacion-del-saspe-y-del-sismate-durante-el-iii-simulacro-nacional-multipeligro
9. **FastAPI:** https://fastapi.tiangolo.com/
10. **React:** https://react.dev/
11. **PostgreSQL:** https://www.postgresql.org/docs/
12. **scikit-learn:** https://scikit-learn.org/stable/
