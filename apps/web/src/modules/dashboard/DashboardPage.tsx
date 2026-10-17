// BLOQUE 1 — Dashboard académico sin indicadores ni eventos ficticios.
import { Link } from 'react-router-dom'
import { Activity, ArrowRight, BellRing, CalendarDays, Database, MapPinned, RadioTower, Ruler, TrendingUp } from 'lucide-react'
import type { LucideIcon } from 'lucide-react'

interface MetricCardProps { title: string; icon: LucideIcon; subtitle: string }

// BLOQUE 2 — KPI reutilizable: — identifica una medición no disponible.
function MetricCard({ title, icon: Icon, subtitle }: MetricCardProps) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-[0_3px_18px_rgba(15,23,42,0.025)] dark:border-[#2b3038] dark:bg-[#1a1e24]">
      <div className="flex items-center justify-between gap-3">
        <p className="text-xs font-medium text-slate-600 dark:text-slate-400">{title}</p>
        <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-slate-100 text-slate-600 dark:bg-[#2a3038] dark:text-slate-300"><Icon size={18} strokeWidth={1.8} /></span>
      </div>
      <p className="mt-4 text-3xl font-semibold tracking-tight text-slate-900 dark:text-slate-50" aria-label="Sin datos">—</p>
      <p className="mt-1 text-[11px] text-slate-500 dark:text-slate-400">{subtitle}</p>
    </div>
  )
}

// BLOQUE 3 — Estados vacíos de gráficas y mapa antes de la Fase 4.
function EmptyVisualization({ type }: { type: 'chart' | 'map' }) {
  const isChart = type === 'chart'
  const Icon = isChart ? TrendingUp : MapPinned
  return (
    <div className="relative flex min-h-[260px] flex-col items-center justify-center overflow-hidden rounded-xl border border-dashed border-slate-200 bg-slate-50/70 px-6 py-9 text-center dark:border-[#363c46] dark:bg-[#15191e]">
      <div className="pointer-events-none absolute inset-0 opacity-50 dark:opacity-30" style={{ backgroundImage: 'linear-gradient(to right, rgba(148,163,184,.1) 1px, transparent 1px), linear-gradient(to bottom, rgba(148,163,184,.1) 1px, transparent 1px)', backgroundSize: '34px 34px' }} aria-hidden="true" />
      <span className="relative z-10 mb-3 flex h-14 w-14 items-center justify-center rounded-2xl bg-white text-slate-400 shadow-sm ring-1 ring-slate-200 dark:bg-[#252b33] dark:text-slate-300 dark:ring-[#343a43]"><Icon size={26} strokeWidth={1.6} /></span>
      <p className="relative z-10 text-sm font-semibold text-slate-700 dark:text-slate-200">{isChart ? 'Aún no hay una serie temporal' : 'Mapa pendiente de integración'}</p>
      <p className="relative z-10 mt-1 max-w-xs text-xs leading-5 text-slate-500 dark:text-slate-400">{isChart ? 'La gráfica aparecerá cuando la API entregue eventos sísmicos verificables.' : 'Aquí se visualizarán eventos georreferenciados provenientes de fuentes identificadas.'}</p>
    </div>
  )
}

// BLOQUE 4 — Panel ejecutivo con estructura estable para conectar datos reales.
export function DashboardPage() {
  return (
    <div className="space-y-6">
      <section className="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
        <div>
          <p className="mb-1 text-xs font-semibold uppercase tracking-[0.16em] text-cyan-700 dark:text-cyan-400">Panel ejecutivo</p>
          <h2 className="text-2xl font-bold tracking-tight text-slate-900 sm:text-[27px] dark:text-slate-50">Visión general</h2>
          <p className="mt-1.5 text-sm text-slate-500 dark:text-slate-400">Monitoreo de eventos observados, fuentes y análisis sísmico.</p>
        </div>
        <span className="inline-flex w-fit items-center gap-2 rounded-lg border border-amber-200 bg-amber-50 px-3 py-2 text-xs font-medium text-amber-800 dark:border-amber-900/50 dark:bg-amber-950/25 dark:text-amber-300"><span className="h-1.5 w-1.5 rounded-full bg-amber-500" />Sin datos sísmicos conectados</span>
      </section>
      <section aria-label="Indicadores principales" className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <MetricCard title="Eventos registrados" icon={Activity} subtitle="Esperando conexión con la fuente" />
        <MetricCard title="Magnitud máxima" icon={TrendingUp} subtitle="Periodo no disponible" />
        <MetricCard title="Profundidad promedio" icon={Ruler} subtitle="Unidad futura: km" />
        <MetricCard title="Alertas operativas" icon={BellRing} subtitle="Reglas todavía no configuradas" />
      </section>
      <section className="grid grid-cols-1 gap-5 xl:grid-cols-[minmax(0,1.25fr)_minmax(0,1fr)]" aria-label="Visualizaciones pendientes">
        <article className="rounded-2xl border border-slate-200 bg-white p-5 shadow-[0_3px_18px_rgba(15,23,42,0.025)] dark:border-[#2b3038] dark:bg-[#1a1e24]">
          <div className="mb-4 flex flex-wrap items-center justify-between gap-2">
            <div><h3 className="text-sm font-semibold">Actividad sísmica</h3><p className="mt-1 text-xs text-slate-500 dark:text-slate-400">Eventos a lo largo del tiempo</p></div>
            <span className="flex items-center gap-1.5 rounded-lg bg-slate-100 px-2.5 py-2 text-[11px] text-slate-500 dark:bg-[#292e36] dark:text-slate-400"><CalendarDays size={14} /> Sin periodo</span>
          </div>
          <EmptyVisualization type="chart" />
        </article>
        <article className="rounded-2xl border border-slate-200 bg-white p-5 shadow-[0_3px_18px_rgba(15,23,42,0.025)] dark:border-[#2b3038] dark:bg-[#1a1e24]">
          <div className="mb-4 flex items-center justify-between gap-3">
            <div><h3 className="text-sm font-semibold">Distribución geográfica</h3><p className="mt-1 text-xs text-slate-500 dark:text-slate-400">Eventos por ubicación</p></div>
            <Link className="inline-flex items-center gap-1.5 text-xs font-semibold text-cyan-700 hover:underline dark:text-cyan-400" to="/mapa-sismico">Ver mapa <ArrowRight size={14} /></Link>
          </div>
          <EmptyVisualization type="map" />
        </article>
      </section>
      <section className="grid grid-cols-1 gap-5 lg:grid-cols-2" aria-label="Estado de módulos">
        <article className="rounded-2xl border border-slate-200 bg-white p-5 dark:border-[#2b3038] dark:bg-[#1a1e24]">
          <div className="flex items-start gap-3">
            <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-cyan-50 text-cyan-700 dark:bg-cyan-950/30 dark:text-cyan-300"><RadioTower size={20} /></span>
            <div className="flex-1"><h3 className="text-sm font-semibold">Fuentes de información</h3><p className="mt-1 text-xs leading-5 text-slate-500 dark:text-slate-400">La fuente sísmica se seleccionará y validará antes de comenzar la ingesta.</p><Link to="/fuentes-datos" className="mt-3 inline-flex items-center gap-1.5 text-xs font-semibold text-cyan-700 hover:underline dark:text-cyan-400">Abrir módulo <ArrowRight size={14} /></Link></div>
          </div>
        </article>
        <article className="rounded-2xl border border-slate-200 bg-white p-5 dark:border-[#2b3038] dark:bg-[#1a1e24]">
          <div className="flex items-start gap-3">
            <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-slate-100 text-slate-600 dark:bg-[#2a3038] dark:text-slate-300"><Database size={20} /></span>
            <div className="flex-1"><h3 className="text-sm font-semibold">Base de datos y modelos</h3><p className="mt-1 text-xs leading-5 text-slate-500 dark:text-slate-400">Supabase y los experimentos de ML se conectarán en sus fases correspondientes.</p><Link to="/modelos-ml" className="mt-3 inline-flex items-center gap-1.5 text-xs font-semibold text-cyan-700 hover:underline dark:text-cyan-400">Abrir módulo <ArrowRight size={14} /></Link></div>
          </div>
        </article>
      </section>
    </div>
  )
}
