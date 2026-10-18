// BLOQUE 1 — Plugins oficiales para la compilación frontend.
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// BLOQUE 2 — Configuración de React y Tailwind CSS 4.
export default defineConfig({ plugins: [react(), tailwindcss()] })
