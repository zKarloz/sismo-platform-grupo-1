# Fase 1 — Anexo de diseño base y navegación

**Estado:** Implementación preparada; validación local pendiente.
**Responsable:** Integrante 1 (base técnica y diseño inicial).
**Continuidad:** Integrante 2 (desarrollo y refinamiento frontend).
**Rama sugerida:** `feature/layout-base`, desde `develop`.

## 1. Objetivo

Implementar una interfaz empresarial inicial con navegación modular, dashboard sin datos ficticios, sidebar adaptable y temas claro y oscuro. Esta tarea complementa el archivo oficial `fase-01-base-tecnica.md`, que continuará siendo el documento de cierre de la Fase 1.

## 2. Stack

- React + TypeScript + Vite (ya disponible).
- Tailwind CSS 4 con plugin `@tailwindcss/vite`.
- `lucide-react` para iconografía.
- `react-router-dom` para navegación.
- Vercel para el futuro despliegue frontend.

## 3. Decisiones de interfaz

- Tema **claro por defecto**, sin depender del tema del sistema operativo.
- Tema oscuro **opcional**, en grises oscuros, activable mediante icono de luna/sol.
- Persistencia del tema con `localStorage` (`sismo-platform-theme`).
- Barra lateral azul marino (tema claro), gris oscuro (tema oscuro); acentos cian.
- Barra superior: navegación, conectividad HTTP de FastAPI y cambio de tema.
- Menú móvil con overlay y cierre mediante botón, selección de ruta o Escape.
- Los 13 módulos del plan técnico tienen ruta propia y pantalla «En desarrollo».
- El dashboard muestra KPIs sin datos, huecos para mapa y gráfica, y paneles de estado.

## 4. Limitaciones deliberadas

- **No hay sismos ficticios** ni cantidades inventadas.
- «API conectada» indica solamente que `GET /health` responde; no demuestra la conexión con Supabase ni la ingesta de eventos.
- Los iconos y el perfil `G1` son provisionales: no representan autenticación real.
- La gráfica, mapa y módulos avanzados se completarán en sus fases correspondientes.
- Las estimaciones experimentales jamás deben confundirse con alertas oficiales.

## 5. Archivos principales

- `apps/web/src/app/navigation.ts`
- `apps/web/src/app/ModulePlaceholder.tsx`
- `apps/web/src/components/layout/AppShell.tsx`
- `apps/web/src/hooks/useTheme.ts`
- `apps/web/src/modules/dashboard/DashboardPage.tsx`
- `apps/web/src/App.tsx`
- `apps/web/src/main.tsx`
- `apps/web/src/index.css`
- `apps/web/vite.config.ts`
- `apps/web/index.html`
- `apps/web/vercel.json`

## 6. Criterios de aceptación (por comprobar)

- [x] `npm run lint` sin errores.
- [x] `npm run build` sin errores.
- [x] Navegación entre los 13 módulos sin pantalla en blanco.
- [x] Sidebar y header con diseño consistente en escritorio.
- [x] Apertura y cierre de menú móvil.
- [x] Tema claro en primera visita.
- [x] Tema oscuro activable y persistente al recargar.
- [x] Etiquetas de ausencia de datos visibles.
- [ ] La API indica conectado/desconectado según `GET /health`.
- [ ] GitHub Actions aprueba el PR.

## 7. Cierre y siguientes pasos

Documentar los resultados de las pruebas en este anexo. Actualizar el archivo `docs/fases/fase-01-base-tecnica.md` con referencia a este prototipo antes de cerrar la Fase 1. Integrar mediante Pull Request hacia `develop`.
