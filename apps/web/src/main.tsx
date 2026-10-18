// BLOQUE 1 — Arranque de React con estilos globales.
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App'
import './index.css'

// BLOQUE 2 — Montaje de la aplicación.
createRoot(document.getElementById('root')!).render(<StrictMode><App /></StrictMode>)
