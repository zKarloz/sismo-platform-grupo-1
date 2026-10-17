// ============================================================
// 1. CONFIGURACIÓN DEL CLIENTE HTTP
// Toda variable VITE_* es visible en el navegador: sin secretos.
// ============================================================
const apiBaseUrl = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/$/, '')

// ============================================================
// 2. CONTRATOS DE RESPUESTA
// ============================================================
export interface ApiHealth {
  status: string
  service: string
}

// ============================================================
// 3. LLAMADA REUTILIZABLE A FASTAPI
// Se conectará a los componentes React en la fase de dashboard.
// ============================================================
export async function getApiHealth(signal?: AbortSignal): Promise<ApiHealth> {
  const response = await fetch(`${apiBaseUrl}/health`, { signal })
  if (!response.ok) {
    throw new Error(`La API respondió con el estado HTTP ${response.status}`)
  }
  return (await response.json()) as ApiHealth
}
