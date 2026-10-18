// BLOQUE 1 — Dependencias del enrutador y layout.
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { allNavigationItems } from './app/navigation'
import { ModulePlaceholder } from './app/ModulePlaceholder'
import { AppShell } from './components/layout/AppShell'
import { DashboardPage } from './modules/dashboard/DashboardPage'

// BLOQUE 2 — Rutas navegables; módulos futuros muestran estado vacío.
export default function App() {
  return (
    <BrowserRouter>
      <AppShell>
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          {allNavigationItems.filter((item) => item.path !== '/').map((item) => (
            <Route key={item.path} path={item.path} element={<ModulePlaceholder module={item} />} />
          ))}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AppShell>
    </BrowserRouter>
  )
}
