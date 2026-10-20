# Fase 1 — Base técnica y diseño UX

> **Proyecto:** Sismo Platform — Sistema Empresarial de Monitoreo Sísmico, Análisis Predictivo y Alertas
> **Documento:** Planificación, implementación, pruebas, despliegue y acta de cierre de la Fase 1
> **Estado:** **CERRADA para el alcance académico de dos semanas**, con pendientes expresamente transferidos
> **Responsable principal:** Integrante 1 — Líder técnico / DevOps / integración
> **Colaboración:** Integrante 2 (frontend y refinamiento UX), integrante 3 (API), integrante 4 (Supabase/PostgreSQL en la etapa de datos)
> **Ejecución y validaciones:** 17–18/10/2026 (según las evidencias compartidas)
> **Consolidación documental:** 19/10/2026
> **Referencia:** _Plan de Desarrollo del Sistema de Monitoreo Sísmico con ML_, sección 9, Fase 1, página 6, y arquitectura/estructura de las páginas 2–3.

## 1. Objetivo y alcance

Establecer una base técnica reproducible, modular y desplegable que permita a los cinco integrantes desarrollar en paralelo: monorepositorio, React + TypeScript + Vite, FastAPI, configuración segura, Docker, integración continua, navegación empresarial y despliegue por HTTPS.

La Fase 1 del PDF incluye además **PostgreSQL, esquema inicial y definición de roles**. En nuestra adaptación académica, la **creación de Supabase, el esquema y las migraciones** se han asignado expresamente al integrante 4 y **no se declaran implementados** aquí. Los roles de trabajo se establecieron a nivel de gestión, pero no existe todavía autenticación ni autorización por rol. Esta excepción queda documentada para no presentar la implementación como un MVP empresarial completo.

**Entregable del PDF:** aplicación base desplegable, estructura modular, esquema inicial y prototipo navegable.
**Resultado de esta fase:** aplicación base y prototipo desplegados; esquema relacional pendiente de la siguiente etapa.

## 2. Decisiones de arquitectura

| Capa              | Tecnología / ubicación                                                  | Estado al cierre                                     |
| ----------------- | ----------------------------------------------------------------------- | ---------------------------------------------------- |
| Frontend          | React + TypeScript + Vite; Tailwind CSS 4; `lucide-react`; React Router | Implementado y probado                               |
| Backend           | Python + FastAPI + Pydantic, configuración de entorno y CORS            | Implementado con rutas mínimas                       |
| Acceso a datos    | SQLAlchemy + Psycopg + Alembic preparados                               | Dependencias instaladas; base de datos sin conectar  |
| Persistencia      | Supabase PostgreSQL                                                     | Pendiente: integrante 4                              |
| Contenedorización | Dockerfile para FastAPI                                                 | Construido y comprobado por HTTP                     |
| CI                | GitHub Actions                                                          | Ejecuciones revisadas exitosas en `main` y `develop` |
| CD / frontend     | Vercel, rama de producción `main`                                       | Desplegado                                           |
| CD / backend      | Render Web Service desde `main`, usando Docker                          | Desplegado                                           |
| Comunicación      | HTTPS y CORS restringido al origen de producción                        | Verificado por HTTP                                  |
| Flujo Git         | `main` producción, `develop` integración, `feature/*` funcionalidades   | Establecido                                          |

## 3. Estructura modular preparada

```text
sismo-platform/
├── apps/
│   └── web/
│       ├── src/
│       │   ├── app/                 # Rutas, navegación y páginas provisionales
│       │   ├── modules/             # Funcionalidades por dominio
│       │   ├── components/          # Layout y componentes reutilizables
│       │   ├── services/            # Cliente HTTP hacia FastAPI
│       │   ├── hooks/               # Estado y tema visual
│       │   ├── schemas/
│       │   ├── types/
│       │   └── lib/
│       └── vercel.json
├── services/
│   ├── api/
│   │   ├── app/
│   │   │   ├── core/config.py
│   │   │   └── main.py
│   │   ├── tests/test_health.py
│   │   ├── Dockerfile
│   │   ├── .dockerignore
│   │   └── requirements.txt
│   ├── ingestion/
│   └── ml/
├── database/
│   ├── migrations/
│   ├── seeds/
│   └── diagrams/
├── tests/
├── infra/
├── docs/
│   ├── fases/
│   └── gestion/
├── .github/workflows/ci.yml
├── .env.example
├── .gitignore
└── README.md
```

Los archivos de código deben contener **comentarios por bloques** y cada fase terminada tendrá **un solo archivo Markdown autosuficiente**. Las carpetas vacías pueden no aparecer en Git hasta que contengan archivos versionados.

## 4. Configuración inicial del proyecto

### 4.1 Frontend

- Proyecto React + TypeScript generado con Vite en `apps/web`.
- Dependencias instaladas mediante `npm install`.
- ESLint disponible y compilación de producción mediante `npm run build`.
- Diseño empresarial con Tailwind CSS y `lucide-react`; rutas mediante `react-router-dom`.

### 4.2 Backend

- Entorno virtual creado en `services/api/.venv`.
- Dependencias iniciales: `fastapi[standard]`, SQLAlchemy, `psycopg[binary]` y Alembic.
- Configuración centralizada: `services/api/app/core/config.py`.
- Aplicación inicial: `services/api/app/main.py`.
- Endpoints existentes:

| Método | Endpoint         | Significado                                            |
| ------ | ---------------- | ------------------------------------------------------ |
| GET    | `/health`        | Verifica disponibilidad HTTP del proceso API           |
| GET    | `/api/v1/status` | Indica que el contrato básico `/api/v1` está operativo |
| GET    | `/docs`          | Interfaz Swagger/OpenAPI generada por FastAPI          |

**Importante:** `/health` **no** verifica conectividad a Supabase ni estado de los proveedores sísmicos.

### 4.3 Seguridad de configuración

- `.gitignore` excluye `node_modules`, `.venv` y archivos `.env` reales.
- `.env.example` documenta variables sin credenciales.
- Los secretos se configuran únicamente en entornos locales protegidos o en las plataformas de despliegue.
- La variable pública `VITE_API_URL` solo contiene la URL del backend, nunca una contraseña ni la cadena de conexión a PostgreSQL.
- Las escrituras y sincronizaciones futuras deben protegerse en el backend: CORS por sí solo **no es autenticación**.

## 5. Diseño UX: base navegable

### 5.1 Principios visuales

- **Tema claro por defecto**, con fondo claro, superficies blancas, navegación azul marino y acentos cian.
- **Tema oscuro opcional**, con grises oscuros en superficies y navegación.
- Selector visual de sol/luna; preferencia persistente en `localStorage` bajo `sismo-platform-theme`.
- Layout profesional con sidebar, encabezado superior e indicador de conexión a la API.
- Diseño adaptable a escritorio y móvil; menú móvil con overlay, cierre mediante botón, selección de ruta o tecla Escape.
- Navegación reservada para los **13 módulos funcionales previstos en el plan**, con pantallas provisionales «En desarrollo» donde corresponde.

### 5.2 Dashboard inicial y estados

- Vista ejecutiva con cuatro espacios de KPI, áreas reservadas para mapa/gráficas y paneles de estado.
- No se incorporaron sismos ficticios, estadísticas inventadas ni estimaciones disfrazadas de alertas oficiales.
- El indicador «API conectada» representa únicamente una respuesta correcta de `GET /health`.
- El avatar/perfil visual `G1` es provisional y **no constituye autenticación real**.
- El integrante 2 continuará refinando accesibilidad, tablas, gráficos, filtros y visualización con datos verificables en las fases funcionales.

### 5.3 Archivos de frontend relevantes

| Archivo                                            | Responsabilidad                           |
| -------------------------------------------------- | ----------------------------------------- |
| `apps/web/src/app/navigation.ts`                   | Menú y navegación por módulos             |
| `apps/web/src/app/ModulePlaceholder.tsx`           | Estados de módulos aún no implementados   |
| `apps/web/src/components/layout/AppShell.tsx`      | Sidebar, header y estado de conexión      |
| `apps/web/src/hooks/useTheme.ts`                   | Selección y persistencia del tema         |
| `apps/web/src/modules/dashboard/DashboardPage.tsx` | Dashboard base y estados vacíos           |
| `apps/web/src/App.tsx`                             | Integración de rutas y aplicación         |
| `apps/web/src/main.tsx`                            | Entrada de React                          |
| `apps/web/src/index.css`                           | Estilos globales y temas                  |
| `apps/web/vite.config.ts`                          | Integración del plugin Tailwind/Vite      |
| `apps/web/index.html`                              | Documento HTML de entrada                 |
| `apps/web/vercel.json`                             | Configuración de navegación SPA en Vercel |

## 6. Procedimiento local reproducible: tres terminales Git Bash

Ejecutar los comandos desde la raíz `sismo-platform`, salvo cuando se indique lo contrario.

### Terminal 1 — Frontend

```bash
cd apps/web
npm install
npm run dev
# URL prevista: http://localhost:5173
```

### Terminal 2 — Backend

```bash
cd services/api
source .venv/Scripts/activate
python -m uvicorn app.main:app --reload --port 8000
# Documentación: http://localhost:8000/docs
```

### Terminal 3 — Pruebas, Docker y Git

```bash
# Comprobar FastAPI y CORS local
curl -i http://localhost:8000/health
curl -i http://localhost:8000/api/v1/status
curl -i -H 'Origin: http://localhost:5173' http://localhost:8000/health

# Pruebas backend (desde services/api)
cd services/api
source .venv/Scripts/activate
python -m unittest discover -s tests -p 'test_*.py' -v
cd ../..

# Lint y build frontend
cd apps/web
npm run lint
npm run build
cd ../..

# Imagen Docker (desde la raíz)
docker build -t sismo-api:0.1 -f services/api/Dockerfile services/api
```

La primera comprobación HTTP inmediata tras `docker run` devolvió `curl: (52) Empty reply from server`; tras revisar el arranque y repetirla con Uvicorn operativo se obtuvo **HTTP 200 OK**. Es consistente con una solicitud demasiado temprana, aunque no se determinó formalmente una causa única.

### Prueba HTTP del contenedor

```bash
docker run -d --name sismo-api -p 8001:10000 -e PORT=10000 sismo-api:0.1
docker ps -a --filter 'name=sismo-api'
docker logs --tail 50 sismo-api
curl --noproxy '*' -i http://127.0.0.1:8001/health
# Respuesta comprobada: HTTP 200; {"status":"ok","service":"sismo-api"}
docker stop sismo-api
docker rm sismo-api
```

## 7. CI/CD y flujo de trabajo con GitHub

- Repositorio: <https://github.com/zKarloz/sismo-platform-grupo-1>.
- Rama predeterminada en GitHub: `develop`.
- Rama de producción usada por Vercel y Render: `main`.
- Rama de funcionalidades: `feature/*` → Pull Request a `develop` → revisión y CI → merge; solo después, promover una versión estable de `develop` a `main` mediante PR.
- Configuración de CI: `.github/workflows/ci.yml`.
- Se notificaron dos workflows exitosos del commit inicial `d6fc189`, uno en cada rama; los nuevos PR deben comprobar sus propios resultados, sin asumir aprobación permanente.
- Evidencias de integración UX: commit de funcionalidad `4148fb9`, merge `df9de0e` a `develop` y merge `13bf6e0` a `main`.
- Los cambios se comprobaron localmente con ESLint, TypeScript y Vite antes de publicarlos.

**Norma de revisión:** no integrar secretos, no editar directamente `main` para funcionalidades y documentar en el PR cómo se verificaron los cambios.

## 8. Despliegue público validado

### 8.1 URLs

| Servicio        | Enlace                                                 | Resultado reportado                                                       |
| --------------- | ------------------------------------------------------ | ------------------------------------------------------------------------- |
| Frontend Vercel | <https://sismo-platform-grupo-1.vercel.app/>           | Aplicación navegable; despliegue de producción `main` en estado **Ready** |
| Backend Render  | <https://sismo-api-grupo-1.onrender.com/>              | API desplegada con Docker                                                 |
| Salud           | <https://sismo-api-grupo-1.onrender.com/health>        | HTTP 200; `status: ok`                                                    |
| API v1          | <https://sismo-api-grupo-1.onrender.com/api/v1/status> | HTTP 200; `api_version: v1`                                               |
| OpenAPI         | <https://sismo-api-grupo-1.onrender.com/docs>          | Documentación accesible                                                   |

### 8.2 Configuración clave

**Render:** servicio web Docker apuntando a `services/api`, `GET /health` como verificación de salud, rama `main`, configuración sensible mediante variables de entorno.

**Vercel:** proyecto Vite con directorio raíz `apps/web`, compilación `npm run build`, salida `dist`, rama **Production = `main`** y `develop` como Preview.

**Frontend:** `VITE_API_URL=https://sismo-api-grupo-1.onrender.com`, habilitada en Production y Preview según la configuración informada.

**Backend CORS:** el origen de producción `https://sismo-platform-grupo-1.vercel.app` se agregó a `CORS_ORIGINS`, junto con los orígenes de desarrollo local. El comando empleado para comprobarlo fue:

```bash
curl -i \
  -H 'Origin: https://sismo-platform-grupo-1.vercel.app' \
  https://sismo-api-grupo-1.onrender.com/health
```

**Resultado comunicado:** respuesta `HTTP/1.1 200 OK` y cabecera
`access-control-allow-origin: https://sismo-platform-grupo-1.vercel.app`.

### 8.3 Incidencia de navegador documentada

En Brave, la interfaz mostró «API desconectada» y DevTools reportó `net::ERR_BLOCKED_BY_CLIENT`. Al desactivar Brave Shields para el sitio, la comunicación funcionó. El fallo era compatible con un bloqueo del cliente; no constituía evidencia de error de la API. Conviene configurar una excepción restringida, en lugar de desactivar globalmente la protección del navegador.

## 9. Matriz de evidencias y criterios de aceptación

Las marcas siguientes corresponden a las **verificaciones comunicadas durante esta fase**, no a una nueva ejecución automatizada en el momento de redactar este documento.

| Criterio                                             | Evidencia                                                   | Estado                    |
| ---------------------------------------------------- | ----------------------------------------------------------- | ------------------------- |
| Estructura modular y variables de entorno de ejemplo | Monorepositorio, `.gitignore`, `.env.example`, README       | Conforme                  |
| React ejecutándose localmente                        | `npm run dev` en `localhost:5173`                           | Conforme                  |
| FastAPI ejecutándose localmente                      | `/health` y `/api/v1/status`, HTTP 200                      | Conforme                  |
| Pruebas automatizadas iniciales                      | 3 pruebas `unittest` aprobadas: salud, estado API, CORS     | Conforme                  |
| Código frontend sin errores de lint                  | `npm run lint` sin incidencias                              | Conforme                  |
| Compilación de producción frontend                   | `npm run build` con TypeScript y Vite                       | Conforme                  |
| Contenedor Docker construido                         | Imagen `sismo-api:0.1` construida                           | Conforme                  |
| Servicio accesible dentro de Docker                  | `127.0.0.1:8001/health`, HTTP 200                           | Conforme                  |
| Variables sensibles excluidas del commit             | `git check-ignore` de `.env`, `.venv` y `node_modules`      | Conforme                  |
| GitHub con integración y CI                          | Ramas publicadas y workflows iniciales exitosos             | Conforme                  |
| Navegación entre módulos y responsive                | Revisión manual de sidebar, menú móvil y rutas              | Conforme                  |
| Temas y persistencia                                 | Claro inicial, oscuro opcional y persistencia tras recargar | Conforme                  |
| Estados del dashboard sin datos ficticios            | Módulos provisionales y ausencia de cifras inventadas       | Conforme                  |
| Sitio público Vercel                                 | Despliegue de `main` Ready                                  | Conforme                  |
| API pública Render                                   | `/health`, `/api/v1/status`, `/docs` accesibles             | Conforme                  |
| Comunicación y CORS de producción                    | `curl` con `Origin` real y header permitido                 | Conforme                  |
| Esquema PostgreSQL de Supabase                       | Delegado al integrante 4, no implementado                   | **Pendiente transferido** |
| Autenticación y roles de acceso reales               | Solo hay representación visual provisional                  | **Pendiente transferido** |

## 10. Riesgos, límites y tareas transferidas

1. **Supabase/PostgreSQL — Integrante 4:** crear el proyecto, definir y versionar esquema/migraciones, configurar conexión segura desde FastAPI; documentar la fase correspondiente.
2. **Seguridad de identidad — Fase 2:** definir roles y autorización real por endpoint; no confundir avatar visual o CORS con acceso autenticado.
3. **Ingesta sísmica — Fase 3:** integrar fuentes verificadas, procedencia, UTC, validación y deduplicación; aún no hay eventos reales almacenados.
4. **Dashboard, mapa y estadísticas reales — Fase 4:** conectar API con datos persistidos; no mostrar resultados inventados.
5. **Calidad y ML — Fases 5–6:** datasets versionados, métricas y limitaciones; no afirmar capacidad de predecir terremotos con precisión.
6. **Alertas y reportes — Fases 7–8:** solo avisos internos de demostración y reportes según el alcance aprobado; nunca presentar alertas oficiales sin integración autorizada.
7. **Pruebas y continuidad — Fase 9:** pruebas de integración/E2E, controles de acceso, respaldos y documentación operativa. No se certifica alta disponibilidad empresarial.
8. **Infraestructura:** un plan gratuito de Render puede introducir latencia tras inactividad; prever pruebas anticipadas y un conjunto persistido para demostraciones.
9. **Navegación y estado:** el indicador de conexión consulta `/health`; no equivale a observabilidad completa ni realiza necesariamente reintentos automáticos.
10. **Fase 0:** la planificación y selección de fuentes están documentadas en `docs/fases/fase-00-alcance.md`; la ratificación por los cinco integrantes debe registrarse cuando ocurra.

## 11. Acta de cierre y aprobación

**Dictamen:** la **Fase 1 queda cerrada para el alcance técnico y de UX reducido del proyecto académico**, con evidencia de ejecución local, pruebas, integración en GitHub y despliegue público. Este cierre es **condicionado en su alcance**: no declara implementados los entregables originalmente previstos de esquema PostgreSQL y acceso por roles. Sus responsables y continuidad quedan identificados en la sección anterior.

**Responsable del cierre técnico:** integrante 1.
**Fecha de consolidación documental:** 19/10/2026.
**Aprobación grupal:** pendiente de ratificación por los demás integrantes; no se atribuyen firmas que no constan.
**Próximo paso:** usar `docs/gestion/backlog-mvp.md` y el documento único de Fase 0 para distribuir las tareas; iniciar las siguientes fases respetando las dependencias.

### Checklist de cierre documental

- [x] Se unificaron la base técnica, el diseño UX y las evidencias/acta de cierre en este documento.
- [x] Se registraron URLs y pruebas comunicadas para Vercel, Render, CI, CORS y Docker.
- [x] Se identificaron expresamente las funcionalidades pospuestas.
- [ ] Integrar este documento mediante PR a `develop` y confirmar CI.
- [ ] Registrar ratificación de los demás integrantes, cuando se produzca.

## 12. Referencias internas

- **Plan técnico original:** _Plan_Desarrollo_Sistema_Monitoreo_Sismico_ML.pdf_, sección 9 (Fase 1), y secciones 4–5 (arquitectura/estructura).
- **Fase 0 (documento único):** `docs/fases/fase-00-alcance.md`.
- **Organización del equipo y backlog:** `docs/gestion/backlog-mvp.md`.
- **Repositorio:** <https://github.com/zKarloz/sismo-platform-grupo-1>.
- **Documentaciones técnicas:** <https://react.dev/>, <https://fastapi.tiangolo.com/>, <https://www.postgresql.org/docs/>.
