def run_supply_simulation(disruption_percent: int, duration_days: int, at_risk_routes: int) -> dict:
    """A deterministic, explainable rule-based simulation; replaceable by a model later."""
    impact = min(95, round(disruption_percent * 0.45 + duration_days * 0.35 + at_risk_routes * 2))
    reserve_day = max(1, 18 - round(impact / 3))
    return {
        "coverage_change_percent": -impact,
        "reserve_target_breached_after_days": reserve_day,
        "affected_routes": at_risk_routes,
        "method": "deterministic rule-based scenario model",
        "recommendation": "Qualify alternative capacity before the reserve target is breached." if impact >= 18 else "Monitor the corridor; current alternatives retain the reserve target.",
    }
