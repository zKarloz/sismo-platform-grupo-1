// BLOQUE 1 — Catálogo de iconos y metadatos de navegación.
import {
  Activity, BellRing, BrainCircuit, ChartNoAxesCombined,
  ClipboardCheck, Database, FileText, FlaskConical,
  LayoutDashboard, MapPinned, RadioTower, ShieldCheck, UsersRound,
} from 'lucide-react'
import type { LucideIcon } from 'lucide-react'

export interface NavigationItem {
  label: string
  path: string
  icon: LucideIcon
  description: string
  phase: string
  responsible: string
}
export interface NavigationGroup { title: string; items: NavigationItem[] }

// BLOQUE 2 — 13 módulos del plan técnico. Pantallas pendientes explícitas.
export const navigationGroups: NavigationGroup[] = [
  {
    title: 'MONITOREO',
    items: [
      { label: 'Dashboard', path: '/', icon: LayoutDashboard, description: 'Indicadores y estado general de la plataforma.', phase: 'Fase 4', responsible: 'Frontend / Backend' },
      { label: 'Eventos sísmicos', path: '/eventos', icon: Activity, description: 'Eventos observados con filtros y trazabilidad.', phase: 'Fase 3', responsible: 'Datos / Backend' },
      { label: 'Mapa sísmico', path: '/mapa-sismico', icon: MapPinned, description: 'Ubicaciones de eventos reportados.', phase: 'Fase 4', responsible: 'Frontend' },
      { label: 'Análisis estadístico', path: '/analisis', icon: ChartNoAxesCombined, description: 'Series temporales y distribuciones históricas.', phase: 'Fase 4', responsible: 'Frontend / Datos' },
      { label: 'Fuentes de datos', path: '/fuentes-datos', icon: RadioTower, description: 'Origen, sincronización y confiabilidad de datos.', phase: 'Fase 3', responsible: 'Datos' },
    ],
  },
  {
    title: 'ANALÍTICA Y ML',
    items: [
      { label: 'Preparación de datos', path: '/preparacion-datos', icon: Database, description: 'Control de calidad y datasets versionados.', phase: 'Fase 5', responsible: 'Datos / ML' },
      { label: 'Modelos de ML', path: '/modelos-ml', icon: BrainCircuit, description: 'Experimentos reproducibles de clasificación y regresión.', phase: 'Fase 6', responsible: 'ML' },
      { label: 'Estimaciones', path: '/estimaciones', icon: FlaskConical, description: 'Estimaciones experimentales y sus limitaciones.', phase: 'Fase 6', responsible: 'ML' },
    ],
  },
  {
    title: 'OPERACIONES',
    items: [
      { label: 'Reglas de alertas', path: '/reglas-alertas', icon: ClipboardCheck, description: 'Reglas operativas sobre eventos recibidos.', phase: 'Fase 7', responsible: 'Backend / DevOps' },
      { label: 'Centro de alertas', path: '/alertas', icon: BellRing, description: 'Seguimiento de alertas verificadas y operativas.', phase: 'Fase 7', responsible: 'Backend / DevOps' },
      { label: 'Reportes', path: '/reportes', icon: FileText, description: 'Exportación de informes y estadísticas.', phase: 'Fase 8', responsible: 'Frontend / Backend' },
      { label: 'Usuarios y roles', path: '/usuarios-roles', icon: UsersRound, description: 'Identidades, permisos y políticas de acceso.', phase: 'Fase 2', responsible: 'Backend' },
      { label: 'Auditoría y configuración', path: '/auditoria', icon: ShieldCheck, description: 'Registro de acciones y configuración del sistema.', phase: 'Fases 2 y 8', responsible: 'Backend / DevOps' },
    ],
  },
]

export const allNavigationItems = navigationGroups.flatMap((group) => group.items)
