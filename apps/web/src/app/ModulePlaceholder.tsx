// BLOQUE 1 — Dependencias y contrato de módulo pendiente.
import { Link } from 'react-router-dom'
import { ArrowLeft, Construction, Info } from 'lucide-react'
import type { NavigationItem } from './navigation'

interface Props { module: NavigationItem }

// BLOQUE 2 — Estado vacío claro y seguro; no se inventan datos.
export function ModulePlaceholder({ module }: Props) {
  const Icon = module.icon
  return (
    <div className="space-y-6">
      <div>
        <p className="mb-1 text-xs font-semibold uppercase tracking-[0.15em] text-cyan-700 dark:text-cyan-400">{module.phase} · Módulo planificado</p>
        <h2 className="text-2xl font-bold tracking-tight sm:text-[27px]">{module.label}</h2>
        <p className="mt-2 max-w-2xl text-sm text-slate-500 dark:text-slate-400">{module.description}</p>
      </div>
      <section className="rounded-2xl border border-slate-200 bg-white px-6 py-14 text-center dark:border-[#2b3038] dark:bg-[#1a1e24]">
        <div className="mx-auto mb-5 flex h-16 w-16 items-center justify-center rounded-2xl bg-cyan-50 text-cyan-700 dark:bg-cyan-950/30 dark:text-cyan-300"><Icon size={27} aria-hidden="true" /></div>
        <span className="inline-flex items-center gap-1.5 rounded-full bg-slate-100 px-3 py-1 text-[11px] font-semibold text-slate-600 dark:bg-[#292e36] dark:text-slate-300"><Construction size={13} /> En desarrollo</span>
        <h3 className="mt-4 text-lg font-semibold">Espacio reservado para {module.label.toLowerCase()}</h3>
        <p className="mx-auto mt-2 max-w-lg text-sm leading-6 text-slate-500 dark:text-slate-400">Este módulo se desarrollará en {module.phase.toLowerCase()}. La navegación y el diseño ya están preparados para que el integrante responsable continúe.</p>
        <div className="mx-auto mt-6 flex max-w-md items-start gap-2 rounded-xl bg-slate-50 p-3 text-left text-xs leading-5 text-slate-600 dark:bg-[#242a31] dark:text-slate-300">
          <Info size={16} className="mt-0.5 shrink-0 text-cyan-600 dark:text-cyan-400" />
          <span>Responsable previsto: <strong>{module.responsible}</strong>. No hay datos reales ni operaciones activas en esta pantalla.</span>
        </div>
        <Link to="/" className="mt-7 inline-flex items-center gap-2 rounded-xl bg-[#102b44] px-4 py-2.5 text-xs font-semibold text-white transition-colors hover:bg-[#174365] dark:bg-cyan-700 dark:hover:bg-cyan-600"><ArrowLeft size={15} /> Volver al dashboard</Link>
      </section>
    </div>
  )
}
