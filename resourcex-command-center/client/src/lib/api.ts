const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1").replace(/\/$/, "");

export type RiskLevel = "Low" | "Watch" | "Elevated" | "High" | string;
export interface Dashboard { resilience_score: number; active_orders: number; at_risk_routes: number; supplier_coverage: number; qualified_sources: number; market_offer_count: number; signals: RiskSignal[]; }
export interface Offer { id: string; resource: string; resource_unit: string; supplier: string; origin: string; quantity: number; unit_price: number; delivery_min_days: number; delivery_max_days: number; risk_level: RiskLevel; status: string; }
export interface Supplier { id: string; name: string; location: string; reliability_score: number; capacity: number; risk_level: RiskLevel; status: string; }
export interface Route { id: string; name: string; origin: string; destination: string; progress: number; eta_days: number; risk_level: RiskLevel; status: string; }
export interface RiskSignal { id: string; title: string; description: string; severity: string; category: string; score: number; status: string; created_at: string; }
export interface Notification { id: string; title: string; body: string; severity: string; is_read: boolean; created_at: string; }
export interface Simulation { id: string; status: string; results: { coverage_change_percent: number; reserve_target_breached_after_days: number; affected_routes: number; recommendation: string; }; created_at: string; }
export interface SearchResult { type: "supplier" | "resource" | "route" | "risk"; id: string; title: string; subtitle: string; }

class ApiError extends Error { constructor(public readonly status: number, message: string) { super(message); } }

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let response: Response;
  try { response = await fetch(`${API_BASE_URL}${path}`, { headers: { "Content-Type": "application/json", ...init?.headers }, ...init }); }
  catch { throw new ApiError(0, "Unable to reach ResourceX API. Check that the backend is running."); }
  if (!response.ok) {
    const body = await response.json().catch(() => null) as { detail?: { message?: string } | string } | null;
    const detail = typeof body?.detail === "string" ? body.detail : body?.detail?.message;
    throw new ApiError(response.status, detail || `Request failed (${response.status})`);
  }
  return response.json() as Promise<T>;
}

export const api = {
  dashboard: () => request<Dashboard>("/dashboard"),
  offers: () => request<Offer[]>("/marketplace/offers"),
  suppliers: () => request<Supplier[]>("/suppliers"),
  routes: () => request<Route[]>("/routes"),
  notifications: () => request<Notification[]>("/notifications"),
  markNotificationRead: (id: string) => request<Notification>(`/notifications/${id}/read`, { method: "PATCH" }),
  search: (query: string) => request<SearchResult[]>(`/search?q=${encodeURIComponent(query)}`),
  simulate: () => request<Simulation>("/simulations", { method: "POST", body: JSON.stringify({ scenario_type: "supplier_export_fall", disruption_percent: 40, duration_days: 15, resource: "Natural gas", route_id: "AE-44" }) }),
};
