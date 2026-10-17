# Fase 1 — Base técnica y diseño UX

**Estado:** En validación (no cerrada automáticamente).  
**Responsable:** Integrante 1 — Líder técnico y DevOps.  
**Colaboración:** Integrante 2 (frontend), integrante 3 (API), integrante 4 (Supabase posteriormente).

## Objetivo

Preparar un monorepositorio reproducible con React/Vite/TypeScript, FastAPI, estructura modular, configuración segura, pruebas iniciales, contenedor Docker y CI básica. El frontend futuro se desplegará en Vercel y la API en Render. La conexión a Supabase pertenece al bloque de datos del integrante 4 y no bloquea esta fase.

## Entregables implementados o previstos

- Carpetas `apps`, `services`, `database`, `tests`, `infra` y `docs` conforme al PDF.
- Frontend React y entorno Python creados durante pasos A–C.
- `.gitignore` revisado, exclusión de `.venv`, `node_modules` y secretos.
- `.env.example` para orientar la configuración sin credenciales.
- `services/api/app/main.py`: aplicación FastAPI, `/health` y `/api/v1/status`.
- `services/api/app/core/config.py`: configuración centralizada y CORS.
- `services/api/tests/test_health.py`: pruebas de salud, versión y CORS.
- `services/api/Dockerfile` y `.dockerignore`.
- `.github/workflows/ci.yml`: compilación de React y pruebas Python.
- `README.md`: instalación, ejecución y rutas.

## Criterios de aceptación — marcar tras probar

- [ ] `npm run dev` inicia React en http://localhost:5173.
- [ ] `npm run lint` se ejecuta sin errores.
- [ ] `npm run build` produce `apps/web/dist`.
- [ ] `python -m uvicorn app.main:app --reload --port 8000` inicia FastAPI.
- [ ] `GET /health` devuelve HTTP 200 y `status=ok`.
- [ ] `GET /api/v1/status` devuelve HTTP 200.
- [ ] La respuesta CORS permite `http://localhost:5173`.
- [ ] `python -m unittest discover -s tests -p 'test_*.py' -v` pasa.
- [ ] `docker build` finaliza sin errores.
- [ ] El contenedor responde desde http://localhost:8001/health.
- [ ] `git status` no muestra `.env`, `.venv` ni `node_modules` para commit.
- [ ] GitHub contiene el commit inicial y se crean `main` y `develop`.
- [ ] Los jobs de GitHub Actions terminan correctamente.

## Comandos de comprobación

**Terminal 1:**

```bash
cd apps/web
npm run dev
```

**Terminal 2:**

```bash
cd services/api
source .venv/Scripts/activate
python -m uvicorn app.main:app --reload --port 8000
```

**Terminal 3:**

```bash
curl -i http://localhost:8000/health
curl -i http://localhost:8000/api/v1/status
curl -i -H 'Origin: http://localhost:5173' http://localhost:8000/health
cd services/api
source .venv/Scripts/activate
python -m unittest discover -s tests -p 'test_*.py' -v
cd ../..
docker build -t sismo-api:0.1 -f services/api/Dockerfile services/api
```

## Evidencias pendientes

Anotar tras las pruebas: fecha, commit, resultado de npm lint/build, salida de tests, resultado del contenedor y enlace al repositorio. Evitar marcar como completadas pruebas no ejecutadas.

## Limitaciones conocidas

- El endpoint `/health` verifica el proceso HTTP, no el estado de Supabase.
- No hay todavía conectores sísmicos, mapa operativo ni autenticación.
- Render y Vercel están **planificados**, pero no desplegados en esta fase.
- HTTPS depende de la infraestructura de producción; localmente usamos HTTP.

## Cierre y aprobación

**Resultado:** Pendiente de validación por el integrante 1.
