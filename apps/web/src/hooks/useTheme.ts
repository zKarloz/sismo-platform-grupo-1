// BLOQUE 1 — Tema claro inicial, persistencia opcional en navegador.
import { useEffect, useState } from 'react'

type Theme = 'light' | 'dark'
const STORAGE_KEY = 'sismo-platform-theme'

function initialTheme(): Theme {
  try { return localStorage.getItem(STORAGE_KEY) === 'dark' ? 'dark' : 'light' }
  catch { return 'light' }
}

// BLOQUE 2 — Sincronización del tema con el elemento html.
export function useTheme() {
  const [theme, setTheme] = useState<Theme>(initialTheme)
  useEffect(() => {
    document.documentElement.classList.toggle('dark', theme === 'dark')
    document.documentElement.style.colorScheme = theme
    try { localStorage.setItem(STORAGE_KEY, theme) }
    catch { /* El tema sigue funcionando aunque localStorage esté bloqueado. */ }
  }, [theme])
  return { theme, toggleTheme: () => setTheme((t) => t === 'light' ? 'dark' : 'light') }
}
