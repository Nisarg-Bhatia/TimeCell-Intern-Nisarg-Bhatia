from typing import Dict, List, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel


class PortfolioRiskEngine:    
    def __init__(self, portfolio_data: Dict):
        self.total_value = portfolio_data.get("total_value_inr", 0)
        self.monthly_expenses = portfolio_data.get("monthly_expenses_inr", 0)
        self.assets = portfolio_data.get("assets", [])

    def run_simulation(self, crash_multiplier: float = 1.0) -> Dict:

        post_crash_total = 0
        risk_scores = {}

        for asset in self.assets:
            name = asset["name"]
            alloc_pct = asset["allocation_pct"]
            expected_drop = asset["expected_crash_pct"] * crash_multiplier
            
            # Math: (Total * Allocation) * (1 - Loss Percentage)
            current_val = self.total_value * (alloc_pct / 100)
            lost_val = current_val * (expected_drop / 100)
            post_crash_total += (current_val + lost_val)
            
            risk_scores[name] = alloc_pct * abs(asset["expected_crash_pct"])

        runway = post_crash_total / self.monthly_expenses if self.monthly_expenses > 0 else 0
        
        return {
            "value": post_crash_total,
            "runway": runway,
            "status": "PASS" if runway > 12 else "FAIL",
            "riskiest": max(risk_scores, key=risk_scores.get)
        }

    def check_concentration(self, threshold: int = 40) -> bool:

        return any(a["allocation_pct"] > threshold for a in self.assets)

def display_dashboard(engine: PortfolioRiskEngine):
    
    chart_table = Table.grid(padding=(0, 2))
    for asset in engine.assets:
        bar = "█" * (asset["allocation_pct"] // 2)
        color = "red" if asset["allocation_pct"] > 40 else "green"
        chart_table.add_row(asset["name"], f"[{color}]{bar}[/]", f"{asset['allocation_pct']}%")
    
    Console().print(Panel(chart_table, title="[bold cyan]Asset Allocation[/]", border_style="cyan"))

    # Risk Table
    full_crash = engine.run_simulation(crash_multiplier=1.0)
    mod_crash = engine.run_simulation(crash_multiplier=0.5)

    res_table = Table(title="Risk Comparison Scenario Table", box=None)
    res_table.add_column("Metric", style="dim")
    res_table.add_column("Full Crash (100%)", justify="right")
    res_table.add_column("Moderate (50%)", justify="right")

    res_table.add_row("Ending Value", f"₹{full_crash['value']:,.0f}", f"₹{mod_crash['value']:,.0f}")
    res_table.add_row("Survival Runway", f"{full_crash['runway']:.1f} months", f"{mod_crash['runway']:.1f} months")
    
    status_color = "green" if full_crash['status'] == "PASS" else "red"
    res_table.add_row("Ruin Test", f"[{status_color}]{full_crash['status']}[/]", f"PASS")

    Console().print(res_table)
    
    if engine.check_concentration():
        Console().print("\n[bold reverse red] WARNING [/] High asset concentration detected (>40%)")
    Console().print(f"[bold yellow]Risk Driver:[/][italic] {full_crash['riskiest']} contributes most to potential losses.")

if __name__ == "__main__":

    raw_portfolio = {
        "total_value_inr": 10_000_000,
        "monthly_expenses_inr": 80_000,
        "assets": [
            {"name": "BTC", "allocation_pct": 30, "expected_crash_pct": -80},
            {"name": "NIFTY50", "allocation_pct": 40, "expected_crash_pct": -40},
            {"name": "GOLD", "allocation_pct": 20, "expected_crash_pct": -15},
            {"name": "CASH", "allocation_pct": 10, "expected_crash_pct": 0},
        ]
    }
    
    risk_engine = PortfolioRiskEngine(raw_portfolio)
    display_dashboard(risk_engine)