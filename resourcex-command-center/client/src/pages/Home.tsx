/**
 * SIGNAL ATLAS — ResourceX command surface
 * Design rules: cartographic dark field, Signal Cyan for intelligence, spatial depth only for real supply relationships.
 */
import { useEffect, useState } from "react";
import { toast } from "sonner";
import { api, type Dashboard, type Offer, type Route as ApiRoute, type SearchResult, type Supplier } from "@/lib/api";
import {
  Activity,
  ArrowUpRight,
  Bell,
  Bot,
  Box,
  BrainCircuit,
  ChevronDown,
  ChevronRight,
  CircleDot,
  Clock3,
  Command,
  Factory,
  FileCheck2,
  Globe2,
  Layers3,
  MapPinned,
  Menu,
  MoreHorizontal,
  Package,
  Radar,
  Search,
  ShieldCheck,
  Ship,
  SlidersHorizontal,
  Sparkles,
  TriangleAlert,
  Truck,
  X,
  Zap,
} from "lucide-react";

const navItems = [
  { label: "Command", icon: Radar },
  { label: "Marketplace", icon: Box },
  { label: "Resources", icon: Layers3 },
  { label: "Suppliers", icon: Factory },
  { label: "Orders", icon: Package },
  { label: "Tracking", icon: Truck },
];

const intelligenceItems = [
  { label: "Risk intelligence", icon: Activity },
  { label: "Digital twin", icon: Globe2 },
  { label: "Simulations", icon: Sparkles },
];

const formatNumber = (value: number) => new Intl.NumberFormat("en-IN").format(value);
const routeTone = (risk: string) => risk === "Low" ? "good" : risk === "Watch" ? "watch" : "risk";

function Mark() {
  return (
    <div className="brand-mark" aria-label="ResourceX home">
      <img src="/manus-storage/resourcex-mark_d28311d4.png" alt="" />
    </div>
  );
}

function NavItem({
  icon: Icon,
  label,
  active,
  onClick,
}: {
  icon: typeof Radar;
  label: string;
  active?: boolean;
  onClick: () => void;
}) {
  return (
    <button className={`nav-item ${active ? "is-active" : ""}`} onClick={onClick}>
      <Icon size={17} strokeWidth={1.8} />
      <span>{label}</span>
      {active && <span className="nav-active-dot" />}
    </button>
  );
}

function NetworkField({ simulation }: { simulation: boolean }) {
  return (
    <div className={`network-field ${simulation ? "is-simulating" : ""}`} aria-label="Global supply network visualization">
      <img className="network-image" src="/manus-storage/resourcex-global-network_af2b9dc5.jpg" alt="Global resource routes across a dark digital twin map" />
      <div className="network-shade" />
      <div className="lat-line line-one" />
      <div className="lat-line line-two" />
      <div className="lat-line line-three" />
      <div className="long-line long-one" />
      <div className="long-line long-two" />
      <div className="network-surface-label label-north">24°N · Arabian corridor</div>
      <div className="network-surface-label label-east">79°E · Bay of Bengal</div>

      <svg className="routes-svg" viewBox="0 0 1000 590" fill="none" aria-hidden="true">
        <defs>
          <linearGradient id="routeGood" x1="0" x2="1">
            <stop stopColor="#38d6ea" stopOpacity="0.2" />
            <stop offset="0.5" stopColor="#54e4b8" />
            <stop offset="1" stopColor="#38d6ea" stopOpacity="0.55" />
          </linearGradient>
          <linearGradient id="routeWarn" x1="0" x2="1">
            <stop stopColor="#ffbd5d" stopOpacity="0.3" />
            <stop offset="0.52" stopColor="#ffbb61" />
            <stop offset="1" stopColor="#ee885a" stopOpacity="0.5" />
          </linearGradient>
          <filter id="glow">
            <feGaussianBlur stdDeviation="4" result="blur" />
            <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>
          </filter>
        </defs>
        <path className="route route-good" d="M 208 181 C 372 86, 494 112, 650 278 S 835 360, 880 188" stroke="url(#routeGood)" />
        <path className="route route-good dim" d="M 170 301 C 348 407, 529 489, 760 375 S 860 272, 910 304" stroke="url(#routeGood)" />
        <path className="route route-watch" d="M 228 438 C 405 358, 544 334, 672 395 S 849 485, 916 419" stroke="url(#routeWarn)" />
        <path className="route route-good muted" d="M 286 146 C 455 250, 527 292, 692 282" stroke="url(#routeGood)" />
        <circle className="flow-dot dot-one" cx="479" cy="123" r="5" fill="#54e4b8" filter="url(#glow)" />
        <circle className="flow-dot dot-two" cx="548" cy="479" r="5" fill="#38d6ea" filter="url(#glow)" />
        <circle className="flow-dot dot-three" cx="590" cy="355" r="5" fill="#ffbb61" filter="url(#glow)" />
      </svg>

      <div className="map-node supplier-node node-oman">
        <span className="node-halo" />
        <span className="node-core node-good" />
        <div className="node-card"><span>SUPPLIER</span><strong>Atlas Energy</strong><small>Oman · LNG</small></div>
      </div>
      <div className="map-node port-node node-mundra">
        <span className="node-halo" />
        <span className="node-core node-good" />
        <div className="node-card"><span>PORT</span><strong>Mundra</strong><small>Normal throughput</small></div>
      </div>
      <div className="map-node port-node node-chennai">
        <span className="node-halo warn" />
        <span className="node-core node-warn" />
        <div className="node-card"><span>PORT</span><strong>Chennai</strong><small>1.8 day congestion</small></div>
      </div>
      <div className="map-node factory-node node-plant">
        <span className="node-halo" />
        <span className="node-core node-blue" />
        <div className="node-card"><span>BUYER</span><strong>Delta Cement</strong><small>12 days reserve</small></div>
      </div>

      <div className="network-legend">
        <span><i className="legend-good" /> flowing normally</span>
        <span><i className="legend-watch" /> monitor</span>
        <span><i className="legend-risk" /> disrupted</span>
      </div>
      <div className="field-instrument"><span>PORT RESILIENCE</span><strong>86</strong><em>/100</em><i /></div>
      <div className="field-scale"><span>0</span><i /><span>2,000 km</span></div>
      <div className="network-controls">
        <button aria-label="Zoom in">+</button>
        <button aria-label="Zoom out">−</button>
        <button aria-label="Recenter"><MapPinned size={14} /></button>
      </div>
    </div>
  );
}

function Metric({ label, value, detail, tone = "cyan" }: { label: string; value: string; detail: string; tone?: "cyan" | "amber" | "green" }) {
  return (
    <div className={`metric metric-${tone}`}>
      <span className="metric-orbit"><i /></span>
      <div>
        <span className="metric-label">{label}</span>
        <div className="metric-value-row">
          <strong>{value}</strong>
          <span className={`metric-pip ${tone}`} />
        </div>
        <span className="metric-detail">{detail}</span>
      </div>
      <span className="metric-ticks" aria-hidden="true" />
    </div>
  );
}

function IntelligenceRail({ onScenario, dashboard }: { onScenario: () => void; dashboard: Dashboard | null }) {
  const signals = dashboard?.signals || [];
  return (
    <aside className="intel-rail">
      <div className="rail-heading">
        <div>
          <span className="eyebrow"><BrainCircuit size={13} /> COPILOT BRIEF</span>
          <h2>Three signals shifted</h2>
        </div>
        <button className="icon-button" aria-label="More brief options"><MoreHorizontal size={18} /></button>
      </div>
      <div className="brief-time"><span className="pulse-dot" /> {signals.length ? "updated from live data" : "loading signals…"}</div>

      <div className="signal-list">
        {signals.map((signal, index) => <button className={`signal-card ${signal.severity === "high" ? "danger-card" : ""}`} key={signal.id}><span className="signal-index">{String(index + 1).padStart(2, "0")}</span><span className="signal-content"><strong>{signal.title}</strong><small>{signal.description}</small></span>{index === 0 ? <span className="signal-score">+{signal.score}</span> : <ChevronRight size={16} />}</button>)}
      </div>

      <div className="impact-card">
        <div className="impact-title"><TriangleAlert size={15} /> EXPOSURE WINDOW</div>
        <div className="impact-top"><strong>12 days</strong><span>critical reserve</span></div>
        <div className="reserve-track"><span /></div>
        <p>Two active routes account for <b>68%</b> of natural gas coverage.</p>
        <button className="quiet-link" onClick={onScenario}>Model a disruption <ArrowUpRight size={14} /></button>
      </div>

      <div className="rail-footnote"><ShieldCheck size={14} /> Predictions are evidence-weighted, not guarantees.</div>
    </aside>
  );
}

function MarketWorkbench({ onCompare, offers }: { onCompare: () => void; offers: Offer[] }) {
  return (
    <section className="market-workbench">
      <div className="workbench-top">
        <div>
          <span className="eyebrow"><Box size={13} /> QUALIFIED MARKET</span>
          <h2>Available supply for your requirements</h2>
        </div>
        <button className="filter-button"><SlidersHorizontal size={16} /> Filter market <span>6</span></button>
      </div>
      <div className="requirement-strip">
        <Search size={18} />
        <span className="search-question">I need <b>10,000 tonnes of Grade A coal</b> in <b>Chennai</b> within <b>15 days</b>.</span>
        <span className="parsed-tag">Coal</span><span className="parsed-tag">10,000 MT</span><span className="parsed-tag">Grade A</span><span className="parsed-tag">≤ 15 days</span>
        <button className="parse-button">Refine <ChevronDown size={14} /></button>
      </div>
      <div className="table-shell">
        <div className="supply-table table-head"><span>RESOURCE / SUPPLIER</span><span>VERIFICATION</span><span>AVAILABILITY</span><span>DELIVERED COST</span><span>DELIVERY</span><span>RISK</span><span /></div>
        {offers.map((offer, index) => (
          <div className="supply-table table-row" key={offer.id}>
            <div className="resource-cell"><span className={`resource-orb orb-${index}`}><Zap size={15} /></span><span><b>{offer.resource}</b><small>{offer.supplier} · {offer.origin}</small></span></div>
            <div className="verified"><ShieldCheck size={15} /><span>Verified</span></div>
            <div className="availability"><b>{formatNumber(offer.quantity)} {offer.resource_unit}</b><small>Grade A</small></div>
            <div className="cost"><b>₹{formatNumber(offer.unit_price)}</b><small>/ {offer.resource_unit} est.</small></div>
            <div className="delivery"><b>{offer.delivery_min_days}–{offer.delivery_max_days} days</b><small>database-backed</small></div>
            <div><span className={`risk-badge ${offer.risk_level.toLowerCase()}`}>{offer.risk_level}</span></div>
            <button className="row-open" aria-label={`View ${offer.supplier}`} onClick={() => toast.info(`${offer.supplier}: ${formatNumber(offer.quantity)} ${offer.resource_unit} available`)}><ArrowUpRight size={16} /></button>
          </div>
        ))}
      </div>
      <div className="workbench-bottom"><span><Bot size={15} /> Atlas Energy is currently the strongest balance of verification, transit time, and coverage.</span><button onClick={onCompare}>Compare suppliers <ArrowUpRight size={15} /></button></div>
    </section>
  );
}

function SupplierComparison({ onBack, suppliers, offers }: { onBack: () => void; suppliers: Supplier[]; offers: Offer[] }) {
  return (
    <section className="comparison-workbench">
      <button className="back-link" onClick={onBack}>← Return to qualified market</button>
      <div className="comparison-title"><div><span className="eyebrow"><Layers3 size={13} /> DECISION WORKBENCH</span><h1>Compare qualified suppliers</h1><p>Natural gas · 25,000 MMBtu · Delivery to Chennai</p></div><button className="primary-action"><Package size={16} /> Request quote</button></div>
      <section className="recommendation-box"><span className="recommendation-rune"><Bot size={19} /></span><div><span className="eyebrow">AI RECOMMENDATION</span><h2>Atlas Energy is the strongest fit for this requirement.</h2><p>It provides the closest quality match, verified terminal documents, and a risk-adjusted arrival window that keeps your reserve above target.</p><button>Show evidence <ArrowUpRight size={14} /></button></div><div className="recommendation-score"><span>FIT SCORE</span><strong>94<span>/100</span></strong><small>high confidence</small></div></section>
      <div className="comparison-table-wrap"><div className="comparison-table comparison-head"><span>SUPPLIER</span><span>QUALIFICATION</span><span>DELIVERED COST</span><span>DELIVERY</span><span>RISK</span><span>RELIABILITY</span><span /></div>{suppliers.slice(0, 3).map((supplier, index) => { const offer = offers.find(item => item.supplier === supplier.name); return <div className={`comparison-table comparison-row ${index === 0 ? "recommended" : ""}`} key={supplier.id}><div className="comparison-supplier"><span className="supplier-badge">{index === 0 ? <Sparkles size={15} /> : <Factory size={15} />}</span><span><b>{supplier.name}{index === 0 && <em>Recommended</em>}</b><small>{supplier.location}</small></span></div><div><b>{supplier.reliability_score}%</b><small>{index === 0 ? "Best coverage" : "Qualified source"}</small></div><div><b>{offer ? `₹${formatNumber(offer.unit_price)}` : "—"}</b><small>/ unit est.</small></div><div><b>{offer ? `${offer.delivery_min_days}–${offer.delivery_max_days}d` : "—"}</b><small>to gate</small></div><div><span className={`risk-badge ${supplier.risk_level.toLowerCase()}`}>{supplier.risk_level}</span></div><div className="reliability-score"><i><span style={{ width: `${supplier.reliability_score}%` }} /></i><b>{supplier.reliability_score}</b></div><button className="select-supplier" onClick={() => toast.success(`${supplier.name} selected for quote preparation`)}>Select <ArrowUpRight size={14} /></button></div>; })}</div>
      <div className="comparison-footnote"><ShieldCheck size={15} /> All candidates meet your minimum verification policy. <button>Adjust qualification policy</button></div>
    </section>
  );
}

function RouteRegister({ routes }: { routes: ApiRoute[] }) {
  return (
    <section className="route-register">
      <div className="route-register-top"><span className="eyebrow"><Ship size={13} /> LIVE ROUTES</span><button className="quiet-link">View all <ArrowUpRight size={13} /></button></div>
      <div className="route-list">
        {routes.map((route) => (
          <button className="route-item" key={route.id} onClick={() => toast.info(`${route.name}: ETA ${route.eta_days} days`)}>
            <span className={`route-state ${routeTone(route.risk_level)}`} />
            <span className="route-main"><b>{route.name}</b><small>{route.status.replaceAll("_", " ")} · {route.id}</small></span>
            <span className="route-progress"><i><span style={{ width: `${route.progress}%` }} /></i><small>{route.progress}%</small></span>
            <ChevronRight size={16} />
          </button>
        ))}
      </div>
    </section>
  );
}

function ScenarioPanel({ close, onRun, running }: { close: () => void; onRun: () => void; running: boolean }) {
  return (
    <div className="scenario-layer">
      <button className="scenario-scrim" aria-label="Close simulator" onClick={close} />
      <section className="scenario-panel" aria-label="What-if crisis simulator">
        <div className="scenario-top"><span className="eyebrow"><Sparkles size={13} /> DIGITAL TWIN</span><button className="icon-button" onClick={close} aria-label="Close simulator"><X size={18} /></button></div>
        <h2>Test a supply disruption</h2>
        <p>Model an event against your current qualified supply network before it becomes operationally real.</p>
        <label>Scenario <div className="scenario-select"><TriangleAlert size={16} /> Major supplier exports fall <ChevronDown size={16} /></div></label>
        <div className="scenario-split"><label>Disruption <div className="scenario-number"><b>40</b><span>%</span></div></label><label>Duration <div className="scenario-number"><b>15</b><span>days</span></div></label></div>
        <label>Affected resource <div className="scenario-select"><Zap size={16} /> Natural gas <ChevronDown size={16} /></div></label>
        <label>Affected corridor <div className="scenario-select"><Globe2 size={16} /> Arabian Sea → Chennai <ChevronDown size={16} /></div></label>
        <div className="scenario-result-preview"><span>ESTIMATED IMPACT</span><div><strong>−18%</strong><small>Supply coverage may fall below reserve target after day 12.</small></div></div>
        <button className="simulate-button" onClick={onRun}><Sparkles size={16} /> {running ? "Simulation running…" : "Run simulation"}</button>
        <div className="scenario-note"><FileCheck2 size={14} /> Uses current route health, verified capacity, and your active orders.</div>
      </section>
    </div>
  );
}

function CommandPalette({ close, onNavigate }: { close: () => void; onNavigate: (destination: string) => void }) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  useEffect(() => {
    if (query.trim().length < 2) { setResults([]); return; }
    const timer = window.setTimeout(() => { api.search(query).then(setResults).catch(() => setResults([])); }, 250);
    return () => window.clearTimeout(timer);
  }, [query]);
  const actions = [
    ["Find qualified supply", "Search resources and suppliers", Search, "Marketplace"],
    ["Compare suppliers", "Open delivery, reliability, and risk comparison", Layers3, "Marketplace"],
    ["Run disruption scenario", "Test a supply-network response", Sparkles, "Command"],
    ["Track shipment", "See current location and ETA", Truck, "Tracking"],
  ] as const;
  return (
    <div className="command-layer" role="dialog" aria-modal="true" aria-label="Command palette">
      <button className="command-scrim" onClick={close} aria-label="Close command palette" />
      <div className="command-palette">
        <div className="command-input"><Search size={18} /><input autoFocus value={query} onChange={event => setQuery(event.target.value)} placeholder="Ask ResourceX or find a command…" /><kbd>ESC</kbd></div>
        {results.length > 0 && <><div className="command-section-label">LIVE RESULTS</div>{results.map(result => <button className="command-action" key={`${result.type}-${result.id}`} onClick={() => { onNavigate(result.type === "supplier" || result.type === "resource" ? "Marketplace" : result.type === "route" ? "Tracking" : "Risk intelligence"); close(); }}><span className="command-action-icon"><Search size={17} /></span><span><b>{result.title}</b><small>{result.subtitle}</small></span><ArrowUpRight size={15} /></button>)}</>}
        <div className="command-section-label">SUGGESTED ACTIONS</div>
        {actions.map(([title, detail, Icon, destination]) => <button className="command-action" key={title} onClick={() => { onNavigate(destination); close(); }}><span className="command-action-icon"><Icon size={17} /></span><span><b>{title}</b><small>{detail}</small></span><ArrowUpRight size={15} /></button>)}
        <div className="command-tip"><Command size={13} /> ResourceX uses page context to pre-fill actions and explain risk.</div>
      </div>
    </div>
  );
}

export default function Home() {
  const [active, setActive] = useState("Command");
  const [paletteOpen, setPaletteOpen] = useState(false);
  const [scenarioOpen, setScenarioOpen] = useState(false);
  const [simulating, setSimulating] = useState(false);
  const [railOpen, setRailOpen] = useState(false);
  const [dashboard, setDashboard] = useState<Dashboard | null>(null);
  const [offers, setOffers] = useState<Offer[]>([]);
  const [suppliers, setSuppliers] = useState<Supplier[]>([]);
  const [routes, setRoutes] = useState<ApiRoute[]>([]);
  const [unreadNotifications, setUnreadNotifications] = useState(0);

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
        event.preventDefault();
        setPaletteOpen(true);
      }
      if (event.key === "Escape") {
        setPaletteOpen(false);
        setScenarioOpen(false);
      }
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, []);

  useEffect(() => {
    let mounted = true;
    Promise.all([api.dashboard(), api.offers(), api.suppliers(), api.routes(), api.notifications()])
      .then(([nextDashboard, nextOffers, nextSuppliers, nextRoutes, notifications]) => {
        if (!mounted) return;
        setDashboard(nextDashboard); setOffers(nextOffers); setSuppliers(nextSuppliers); setRoutes(nextRoutes);
        setUnreadNotifications(notifications.filter(notification => !notification.is_read).length);
      })
      .catch((error: unknown) => { if (mounted) toast.error(error instanceof Error ? error.message : "Could not load command-center data"); });
    return () => { mounted = false; };
  }, []);

  const runSimulation = async () => {
    setSimulating(true);
    try {
      const simulation = await api.simulate();
      toast.success(`Scenario complete: ${simulation.results.coverage_change_percent}% coverage change; reserve target after day ${simulation.results.reserve_target_breached_after_days}.`);
      setSimulating(false);
      setScenarioOpen(false);
    } catch (error) {
      setSimulating(false);
      toast.error(error instanceof Error ? error.message : "Simulation could not be completed");
    }
  };

  const showNotifications = async () => {
    try {
      const notifications = await api.notifications();
      const unread = notifications.filter(notification => !notification.is_read);
      await Promise.all(unread.map(notification => api.markNotificationRead(notification.id)));
      setUnreadNotifications(0);
      toast.info(unread.length ? unread.map(notification => notification.title).join(" · ") : "No new notifications");
    } catch (error) { toast.error(error instanceof Error ? error.message : "Could not load notifications"); }
  };

  const isMarketplace = active === "Marketplace";
  const isComparison = active === "Suppliers";

  return (
    <main className="app-shell">
      <aside className="side-nav">
        <div className="nav-brand"><Mark /><div className="brand-name">resource<span>x</span></div></div>
        <div className="nav-group"><span className="nav-caption">WORKSPACE</span>{navItems.map((item) => <NavItem key={item.label} {...item} active={active === item.label} onClick={() => setActive(item.label)} />)}</div>
        <div className="nav-group intelligence-group"><span className="nav-caption">INTELLIGENCE</span>{intelligenceItems.map((item) => <NavItem key={item.label} {...item} active={active === item.label} onClick={() => setActive(item.label)} />)}</div>
        <div className="nav-bottom"><button className="profile-button"><span className="avatar">DR</span><span><b>Delta Resources</b><small>Buyer workspace</small></span><ChevronDown size={14} /></button></div>
      </aside>

      <section className="main-canvas">
        <header className="topbar">
          <button className="mobile-menu" onClick={() => setRailOpen(!railOpen)} aria-label="Open navigation"><Menu size={20} /></button>
          <div className="workspace-crumb"><span>DELTA RESOURCES</span><ChevronRight size={13} /><b>{active}</b></div>
          <div className="topbar-actions"><button className="command-trigger" onClick={() => setPaletteOpen(true)}><Command size={15} /><span>Ask or command</span><kbd>⌘ K</kbd></button><button className="icon-button notification" onClick={showNotifications} aria-label="Read notifications"><Bell size={18} />{unreadNotifications > 0 && <i />}</button><button className="operator"><span>DR</span><ChevronDown size={14} /></button></div>
        </header>

        {isMarketplace ? <MarketWorkbench onCompare={() => setActive("Suppliers")} offers={offers} /> : isComparison ? <SupplierComparison onBack={() => setActive("Marketplace")} suppliers={suppliers} offers={offers} /> : <>
          <section className="command-header">
            <div><span className="eyebrow"><CircleDot size={13} /> NETWORK STATUS · LIVE</span><h1>One corridor needs action.</h1><p>Your network remains within reserve target. <b>Review the Chennai natural-gas corridor before its disruption window opens.</b></p></div>
            <div className="header-actions"><button className="ghost-action" onClick={() => setActive("Marketplace")}><Box size={16} /> Qualified market</button><button className="primary-action" onClick={() => setScenarioOpen(true)}><Sparkles size={16} /> What if?</button></div>
          </section>
          <section className="metric-row">
            <Metric label="RESILIENCE SCORE" value={dashboard ? String(dashboard.resilience_score) : "—"} detail="derived from route health" tone="green" />
            <Metric label="ACTIVE ORDERS" value={dashboard ? String(dashboard.active_orders) : "—"} detail="confirmed and in transit" />
            <Metric label="AT-RISK ROUTES" value={dashboard ? String(dashboard.at_risk_routes).padStart(2, "0") : "—"} detail="need review" tone="amber" />
            <Metric label="SUPPLIER COVERAGE" value={dashboard ? `${dashboard.supplier_coverage}%` : "—"} detail={`${dashboard?.qualified_sources ?? 0} qualified sources`} tone="green" />
          </section>
          <section className="command-grid">
            <div className="atlas-area"><div className="atlas-topline"><span className="eyebrow"><Globe2 size={13} /> GLOBAL RESOURCE FIELD</span><span className="live-coordinates"><i /> 20.5937° N, 78.9629° E</span></div><NetworkField simulation={simulating} /><div className="field-footer"><span><Clock3 size={14} /> Network state re-evaluated continuously</span><button onClick={() => setActive("Digital twin")}>Open digital twin <ArrowUpRight size={14} /></button></div></div>
            <IntelligenceRail onScenario={() => setScenarioOpen(true)} dashboard={dashboard} />
          </section>
          <div className="lower-grid"><RouteRegister routes={routes} /><section className="supply-brief"><div className="supply-brief-bg" /><div><span className="eyebrow">MARKET SCAN</span><h2>Compatible supply<br />is within reach.</h2><p>{dashboard?.market_offer_count ?? 0} active offers match your delivery profile and verification policy.</p><button onClick={() => setActive("Marketplace")}>Inspect supply <ArrowUpRight size={15} /></button></div><img src="/manus-storage/resourcex-port-signal_81caa41c.jpg" alt="Industrial resource port" /></section></div>
        </>}
      </section>

      {railOpen && <div className="mobile-nav-overlay"><button className="mobile-nav-scrim" onClick={() => setRailOpen(false)} /><div className="mobile-nav-panel"><div className="nav-brand"><Mark /><div className="brand-name">resource<span>x</span></div><button className="icon-button" onClick={() => setRailOpen(false)}><X size={18} /></button></div>{navItems.map((item) => <NavItem key={item.label} {...item} active={active === item.label} onClick={() => { setActive(item.label); setRailOpen(false); }} />)}{intelligenceItems.map((item) => <NavItem key={item.label} {...item} active={active === item.label} onClick={() => { setActive(item.label); setRailOpen(false); }} />)}</div></div>}
      {paletteOpen && <CommandPalette close={() => setPaletteOpen(false)} onNavigate={setActive} />}
      {scenarioOpen && <ScenarioPanel close={() => setScenarioOpen(false)} onRun={runSimulation} running={simulating} />}
    </main>
  );
}
