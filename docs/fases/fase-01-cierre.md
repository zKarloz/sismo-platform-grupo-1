# Fase 1 — Acta de cierre: base técnica y diseño UX

**Proyecto:** Sistema Empresarial de Monitoreo Sísmico, Análisis Predictivo y Alertas
**Estado:** Cerrada para el alcance académico acordado; dependencias transferidas identificadas
**Responsable:** Integrante 1 — Líder técnico y DevOps
**Fecha de validación:** 17 de octubre de 2026 (confirmaciones locales y de producción compartidas por el equipo)
**Referencia:** Plan de desarrollo, Fase 1 (sección 9, página 6)

## 1. Alcance de este cierre

Se cierra la **base técnica y el prototipo UX navegable** correspondiente a la adaptación académica de dos semanas. El PDF original también prevé PostgreSQL, un esquema inicial y convenciones de roles; la definición/implementación de PostgreSQL se ha delegado al integrante 4 para su continuación. Este cierre **no certifica** la base de datos, la seguridad empresarial, la ingesta ni los modelos ML.

## 2. Arquitectura validada

- **Monorepositorio:** `apps/web`, `services/api`, `services/ingestion`, `services/ml`, `database`, `tests`, `infra`, `docs`.
- **Frontend:** React + TypeScript + Vite + Tailwind CSS + lucide-react; tema claro predeterminado y tema oscuro opcional, navegación y layout empresarial.
- **Backend:** Python + FastAPI; endpoints REST mínimos; configuración de entornos y CORS.
- **Contenedorización:** Dockerfile del backend, imagen `sismo-api:0.1` probada localmente.
- **CI:** GitHub Actions con comprobaciones de frontend y backend.
- **Despliegue:** Vercel para frontend y Render para API, ambos con HTTPS.
- **Persistencia prevista:** Supabase PostgreSQL (integración pendiente, integrante 4).

## 3. Evidencias verificadas

| Comprobación     | Evidencia comunicada                                                                      | Resultado                           |
| ---------------- | ----------------------------------------------------------------------------------------- | ----------------------------------- |
| React dev server | Frontend iniciado localmente                                                              | Conforme                            |
| FastAPI local    | `/health`, `/api/v1/status` devuelven JSON esperado                                       | Conforme                            |
| Pruebas Python   | 3 pruebas de `unittest` aprobadas                                                         | Conforme                            |
| ESLint           | `npm run lint` sin errores                                                                | Conforme                            |
| Build Vite       | `npm run build` completado                                                                | Conforme                            |
| Docker build     | Imagen `sismo-api:0.1` construida                                                         | Conforme                            |
| Docker HTTP      | `curl` a `127.0.0.1:8001/health` devuelve HTTP 200                                        | Conforme                            |
| GitHub           | `main` y `develop` publicadas; PR del diseño integrado                                    | Conforme                            |
| CI               | Se reportaron ejecuciones exitosas en `main` y `develop`                                  | Conforme para ejecuciones revisadas |
| UX               | Navegación y cambio de temas probados manualmente                                         | Conforme                            |
| Render           | `/health`, `/api/v1/status` y `/docs` accesibles públicamente                             | Conforme                            |
| Vercel           | Producción `main` en estado Ready                                                         | Conforme                            |
| CORS             | Solicitud con `Origin` de Vercel recibe HTTP 200 y `access-control-allow-origin` correcto | Conforme                            |
| Navegador Brave  | Bloqueo inicial de solicitud resuelto al desactivar Shields para el sitio                 | Incidencia identificada             |

## 4. URLs de los entornos públicos

- Frontend producción: <https://sismo-platform-grupo-1.vercel.app/>
- Backend producción: <https://sismo-api-grupo-1.onrender.com/>
- Salud: <https://sismo-api-grupo-1.onrender.com/health>
- Versión de API: <https://sismo-api-grupo-1.onrender.com/api/v1/status>
- Swagger/OpenAPI: <https://sismo-api-grupo-1.onrender.com/docs>

**Convenciones:** `main` es producción, `develop` integración, `feature/*` ramas de trabajo. GitHub tiene `develop` como rama predeterminada. Evitar publicar cambios funcionales en `main` sin PR y comprobaciones.

## 5. Pendientes explícitos transferidos

1. **Fase 0:** cerrar fuente sísmica, derechos de uso, volumen/frecuencia, usuarios iniciales, riesgos, casos de uso y backlog.
2. **Integrante 4 / base de datos:** diseñar y versionar el **esquema PostgreSQL inicial**, crear el proyecto Supabase, migraciones y validar conexión FastAPI → PostgreSQL. **No está implementado** en este cierre.
3. **Fase 2:** autenticación/autorización y auditoría (el indicador o avatar visual actual no representa una identidad autenticada).
4. **Fases 3–4:** ingesta, dashboard real, tabla y mapa con trazabilidad de fuentes.
5. **Fases 5–8:** calidad de datos, experimentos ML, alertas basadas en eventos reportados, reportes y administración según prioridades de la Fase 0.
6. **Fase 9:** pruebas finales integrales, backup/restauración y documentación operativa conforme al alcance disponible.

## 6. Riesgos y limitaciones

- El `GET /health` prueba disponibilidad HTTP, **no** disponibilidad de Supabase.
- La aplicación aún no ofrece monitoreo de eventos reales ni predicción sísmica; evitar cualquier promesa de fecha, lugar o magnitud exactos de sismos futuros.
- En Brave, ciertas protecciones pueden impedir solicitudes entre dominios (`ERR_BLOCKED_BY_CLIENT`).
- Si se utiliza un servicio de Render gratuito, puede existir latencia de arranque tras inactividad.
- No subir credenciales, tokens ni cadenas de conexión completas a GitHub ni a documentos.
- La protección de ramas y las revisiones deben verificarse en la configuración del repositorio.

## 7. Aprobación y continuidad

**Dictamen:** **FASE 1 CERRADA para el alcance académico reducido y validado**, con pendientes de PostgreSQL y roles reales expresamente transferidos. La Fase 0 permanece **ABIERTA** hasta que se complete su documento de alcance y decisiones.

**Responsable de aprobación:** Integrante 1.
**Evidencia final adicional opcional:** enlace a los workflows y PR definitivos; capturas de los dos despliegues.

---

> Nota de consistencia: actualizar el campo «Estado» y las referencias de despliegue de `fase-01-base-tecnica.md` y `fase-01-diseno-base.md`; este acta los complementa sin sustituir los documentos existentes.
