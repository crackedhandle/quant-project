import json
from pathlib import Path

r = Path("results")
out = r / "system_summary.json"

summary = {}

# 1) Add metrics
for file in ["final_metrics.json", "per_alpha_metrics.json", "portfolio_weights.json"]:
    path = r / file
    if path.exists():
        with open(path, "r", encoding="utf8") as f:
            summary[file.replace(".json", "")] = json.load(f)

# 2) Add portfolio results snapshot
pnl_path = r / "portfolio_backtest.csv"
if pnl_path.exists():
    import pandas as pd
    df = pd.read_csv(pnl_path)
    summary["portfolio_final"] = {
        "equal_final_cum": float(df["cum_equal"].iloc[-1]),
        "vol_scaled_final_cum": float(df["cum_vol_scaled"].iloc[-1])
    }

with open(out, "w", encoding="utf8") as f:
    json.dump(summary, f, indent=2)

print("✅ Saved: results/system_summary.json")
