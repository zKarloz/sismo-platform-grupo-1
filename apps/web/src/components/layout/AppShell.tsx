// BLOQUE 1 — Dependencias, contratos y conexión con FastAPI.
import { useEffect, useState } from 'react'
import type { ReactNode } from 'react'
import { Link, NavLink, useLocation } from 'react-router-dom'
import { Activity, ChevronRight, Menu, Moon, Sun, X } from 'lucide-react'
import { allNavigationItems, navigationGroups } from '../../app/navigation'
import { useTheme } from '../../hooks/useTheme'
import { getApiHealth } from '../../services/api'

type ApiStatus = 'checking' | 'online' | 'offline'
interface SidebarProps { onNavigate: () => void }

// BLOQUE 2 — Menú común del escritorio y móvil, según las 13 rutas.
function SidebarNavigation({ onNavigate }: SidebarProps) {
  return (
    <div className="flex h-full flex-col bg-[#102b44] text-slate-200 dark:bg-[#181b20]">
      <Link to="/" onClick={onNavigate} className="flex items-center gap-3 border-b border-white/10 px-5 py-[21px] hover:bg-white/5" aria-label="Volver al dashboard">
        <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-cyan-400/15 text-cyan-300 ring-1 ring-cyan-300/20"><Activity size={23} strokeWidth={2.2} aria-hidden="true" /></span>
        <span className="min-w-0">
          <span className="block truncate text-[15px] font-bold tracking-tight text-white">Sismo Platform</span>
          <span className="block text-[11px] tracking-[0.08em] text-slate-400">MONITOREO Y ANALÍTICA</span>
        </span>
      </Link>
      <nav className="flex-1 space-y-6 overflow-y-auto px-3 py-5" aria-label="Navegación principal">
        {navigationGroups.map((group) => (
          <section key={group.title} aria-label={group.title}>
            <p className="px-3 pb-2 text-[10px] font-semibold tracking-[0.17em] text-slate-400">{group.title}</p>
            <div className="space-y-0.5">
              {group.items.map((item) => {
                const Icon = item.icon
                return (
                  <NavLink key={item.path} to={item.path} end={item.path === '/'} onClick={onNavigate}
                    className={({ isActive }) => [
                      'group flex min-h-10 items-center gap-3 rounded-lg px-3 py-2 text-[13px] font-medium transition-colors',
                      isActive ? 'bg-cyan-400/15 text-white ring-1 ring-inset ring-cyan-300/20' : 'text-slate-300 hover:bg-white/7 hover:text-white',
                    ].join(' ')}>
                    <Icon size={17} className="shrink-0 text-cyan-200/90" strokeWidth={1.8} aria-hidden="true" />
                    <span className="flex-1 leading-5">{item.label}</span>
                  </NavLink>
                )
              })}
            </div>
          </section>
        ))}
      </nav>
      <div className="border-t border-white/10 px-5 py-4">
        <p className="flex items-center gap-2 text-xs text-slate-300"><span className="h-2 w-2 rounded-full bg-cyan-400" />Entorno académico</p>
        <p className="mt-1 text-[11px] text-slate-400">Fase 1 · Prototipo visual</p>
      </div>
    </div>
  )
}

// BLOQUE 3 — Comprobar solo la disponibilidad de la API; no de Supabase.
function useApiStatus(): ApiStatus {
  const [status, setStatus] = useState<ApiStatus>('checking')
  useEffect(() => {
    const controller = new AbortController()
    getApiHealth(controller.signal).then(() => setStatus('online')).catch((error: unknown) => {
      if (error instanceof Error && error.name === 'AbortError') return
      setStatus('offline')
    })
    return () => controller.abort()
  }, [])
  return status
}

// BLOQUE 4 — Estructura adaptable, navegación móvil y botón de tema.
export function AppShell({ children }: { children: ReactNode }) {
  const { pathname } = useLocation()
  const selected = allNavigationItems.find((item) => item.path === pathname) ?? allNavigationItems[0]
  const { theme, toggleTheme } = useTheme()
  const apiStatus = useApiStatus()
  const [mobileOpen, setMobileOpen] = useState(false)

  useEffect(() => {
    if (!mobileOpen) return
    const onEscape = (event: KeyboardEvent) => { if (event.key === 'Escape') setMobileOpen(false) }
    window.addEventListener('keydown', onEscape)
    return () => window.removeEventListener('keydown', onEscape)
  }, [mobileOpen])

  return (
    <div className="min-h-screen bg-[#f5f7fb] text-slate-900 transition-colors duration-200 dark:bg-[#0f1115] dark:text-slate-100">
      {/* BLOQUE 4.1 — Sidebar del escritorio. */}
      <aside className="fixed inset-y-0 left-0 z-30 hidden w-64 lg:block" aria-label="Barra lateral"><SidebarNavigation onNavigate={() => undefined} /></aside>

      {/* BLOQUE 4.2 — Menú móvil con capa de cierre. */}
      {mobileOpen && (
        <div className="fixed inset-0 z-50 lg:hidden">
          <button type="button" className="absolute inset-0 bg-slate-950/60" onClick={() => setMobileOpen(false)} aria-label="Cerrar menú lateral" />
          <aside className="relative h-full w-[min(86vw,290px)] shadow-2xl" aria-label="Menú móvil">
            <SidebarNavigation onNavigate={() => setMobileOpen(false)} />
            <button type="button" className="absolute right-3 top-4 rounded-lg p-2 text-white hover:bg-white/10" onClick={() => setMobileOpen(false)} aria-label="Cerrar menú"><X size={19} /></button>
          </aside>
        </div>
      )}
      <div className="min-h-screen lg:pl-64">
        {/* BLOQUE 4.3 — Encabezado, estado de FastAPI y selector de tema. */}
        <header className="sticky top-0 z-20 flex h-[74px] items-center justify-between gap-3 border-b border-slate-200 bg-white/95 px-4 backdrop-blur md:px-8 dark:border-[#2b3038] dark:bg-[#181b20]/95">
          <div className="flex min-w-0 items-center gap-3">
            <button type="button" className="rounded-lg border border-slate-200 p-2 text-slate-600 hover:bg-slate-50 lg:hidden dark:border-[#353b44] dark:text-slate-300 dark:hover:bg-[#262b32]" onClick={() => setMobileOpen(true)} aria-label="Abrir menú de navegación" aria-expanded={mobileOpen}><Menu size={19} /></button>
            <div className="min-w-0">
              <div className="hidden items-center gap-1.5 text-[11px] text-slate-500 sm:flex dark:text-slate-400"><span>Plataforma</span><ChevronRight size={12} /><span className="truncate">{selected.label}</span></div>
              <h1 className="truncate text-base font-semibold tracking-tight sm:text-lg">{selected.label}</h1>
            </div>
          </div>
          <div className="flex shrink-0 items-center gap-2 sm:gap-3">
            <span className="hidden items-center gap-2 rounded-full border border-slate-200 px-3 py-1.5 text-[11px] font-medium text-slate-600 sm:flex dark:border-[#353b44] dark:text-slate-300" title="Verifica FastAPI, no la fuente sísmica">
              <span className={`h-2 w-2 rounded-full ${apiStatus === 'online' ? 'bg-emerald-500' : apiStatus === 'offline' ? 'bg-rose-500' : 'bg-amber-400'}`} />
              {apiStatus === 'online' ? 'API conectada' : apiStatus === 'offline' ? 'API desconectada' : 'Comprobando API'}
            </span>
            <button type="button" onClick={toggleTheme}
              className="flex h-10 w-10 items-center justify-center rounded-xl border border-slate-200 text-slate-700 transition-colors hover:bg-slate-100 dark:border-[#353b44] dark:text-slate-100 dark:hover:bg-[#262b32]"
              title={theme === 'light' ? 'Activar tema oscuro' : 'Activar tema claro'} aria-label={theme === 'light' ? 'Activar tema oscuro' : 'Activar tema claro'}>
              {theme === 'light' ? <Moon size={18} aria-hidden="true" /> : <Sun size={18} aria-hidden="true" />}
            </button>
            <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-[#102b44] text-xs font-bold text-white dark:bg-[#323843]" title="Perfil de demostración; autenticación pendiente" aria-label="Perfil de demostración">G1</span>
          </div>
        </header>
        {/* BLOQUE 4.4 — Contenido y aclaración de responsabilidad científica. */}
        <main id="contenido-principal" className="mx-auto w-full max-w-[1600px] px-4 pb-10 pt-7 md:px-8 md:pt-8">{children}</main>
        <footer className="mx-auto max-w-[1600px] px-4 pb-7 text-[11px] text-slate-500 md:px-8">Sismo Platform · Proyecto académico · Ninguna estimación experimental equivale a una alerta oficial.</footer>
      </div>
    </div>
  )
}
