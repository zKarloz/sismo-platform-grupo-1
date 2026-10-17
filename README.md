# Sismo Platform | Sistema de Monitoreo Sísmico

Monorepositorio académico, desarrollado por un equipo de **cinco integrantes** durante **dos semanas**. Arquitectura conforme al plan técnico: **React + TypeScript + Vite**, **Python + FastAPI**, **PostgreSQL en Supabase** y experimentos de Machine Learning en Python.

> **Aviso importante:** el software distingue eventos observados, estimaciones experimentales y comunicados oficiales. No predice con certeza cuándo, dónde ni con qué magnitud ocurrirá un terremoto, ni reemplaza al IGP o INDECI.

## Arquitectura

- `apps/web`: aplicación React (posterior despliegue en **Vercel**).
- `services/api`: API FastAPI (posterior despliegue en **Render** mediante Docker).
- `services/ingestion`: adaptadores de fuentes sísmicas (a implementar).
- `services/ml`: preparación, entrenamiento y evaluación ML (a implementar).
- `database`: migraciones SQL, semillas y diagramas (a cargo del integrante 4).
- `docs/fases`: actas técnicas y criterios de aceptación por fase.
- `.github/workflows/ci.yml`: CI básico en pushes y pull requests.

## Requisitos

- Git Bash en Windows, Node.js 24+, npm, Python 3.14, Git.
- Docker Desktop para probar la imagen del backend (no es obligatorio para ejecutar FastAPI localmente).
- Supabase **no es necesario para iniciar la Fase 1**.

## Preparación inicial

Ejecutar desde la raíz del repositorio:

```bash
# Frontend
cd apps/web
npm ci
cp .env.example .env
cd ../..

# Backend
py -3 -m venv services/api/.venv
source services/api/.venv/Scripts/activate
python -m pip install -r services/api/requirements.txt
cp .env.example services/api/.env
```

> En Linux/macOS usar `python3 -m venv ...` y `source services/api/.venv/bin/activate`.

## Tres terminales Git Bash

**Terminal 1 — Frontend:**

```bash
cd apps/web
npm run dev
```

Aplicación: http://localhost:5173

**Terminal 2 — Backend:**

```bash
cd services/api
source .venv/Scripts/activate
python -m uvicorn app.main:app --reload --port 8000
```

API: http://localhost:8000/health — Documentación: http://localhost:8000/docs

**Terminal 3 — Pruebas:**

```bash
cd services/api
source .venv/Scripts/activate
python -m unittest discover -s tests -p 'test_*.py' -v
```

Para comprobar CORS:

```bash
curl -i -H 'Origin: http://localhost:5173' http://localhost:8000/health
```

## Docker (backend)

Con Docker Desktop iniciado, desde la raíz del repositorio:

```bash
docker build -t sismo-api:0.1 -f services/api/Dockerfile services/api
docker run --rm --name sismo-api -p 8001:10000 -e PORT=10000 sismo-api:0.1
```

En otra terminal o navegador: http://localhost:8001/health

> El backend Dockerizado no requiere Supabase en esta fase. El endpoint `/health` solo informa que FastAPI responde.

## Variables y despliegue futuro

- `services/api/.env` se configura a partir del `.env.example` de la raíz (solo local; nunca se sube a Git).
- `apps/web/.env` se configura desde `apps/web/.env.example` (solo URL pública de API).
- Render: servicio Docker con root directory `services/api`; Dockerfile `Dockerfile`; contexto `.`; endpoint de salud `/health`; definir `CORS_ORIGINS` con la URL HTTPS de Vercel.
- Vercel: root directory `apps/web`, preset **Vite**, build `npm run build`, output `dist`, `VITE_API_URL` apuntando a HTTPS de Render.
- Supabase: el integrante 4 aportará la configuración segura de PostgreSQL a través de variables privadas; no añadir contraseñas al frontend.

## CI y convención Git

- `main`: versiones estables y presentaciones.
- `develop`: integración del grupo.
- `feature/*`: trabajo individual mediante pull requests.
- CI valida compilación de React y los tests de FastAPI.

## Documentación de fases

Consultar `docs/fases/fase-00-alcance.md` y `docs/fases/fase-01-base-tecnica.md`. Cada fase se marca como cerrada **solo cuando sus criterios de aceptación se validan**.
