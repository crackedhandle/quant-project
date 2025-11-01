import pandas as pd
import matplotlib.pyplot as plt
import quantstats as qs
import json, os

# === Load the latest results ===
results_path = max(
    [f for f in os.listdir("results") if f.endswith(".json")],
    key=lambda f: os.path.getmtime(os.path.join("results", f))
)
with open(os.path.join("results", results_path)) as f:
    data = json.load(f)

# === Convert to simple DataFrame ===
pnl_series = pd.Series(data)
pnl_series.plot(kind="bar", title="Portfolio PnL Breakdown")
plt.tight_layout()
plt.savefig("results/portfolio_pnl_bar.png")
plt.show()

# === Generate quantstats report ===
qs.extend_pandas()
returns = pd.Series([data.get(k, 0) for k in data if "pnl" in k])
returns.index = [k for k in data if "pnl" in k]
qs.reports.html(returns, output="results/quantstats_report.html", title="Portfolio Performance Report")
print(f"\nVisualization saved to results/portfolio_pnl_bar.png and quantstats_report.html")
