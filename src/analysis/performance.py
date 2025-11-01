import json
import math
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

results_dir = Path("results")
results_dir.mkdir(exist_ok=True)

# --- Load portfolio aggregated backtest
agg_path = results_dir / "portfolio_aggregated.csv"
if not agg_path.exists():
    raise SystemExit(f"Missing file: {agg_path}. Run aggregation step first.")

df = pd.read_csv(agg_path)
# If PnL column exists already, use it; otherwise compute from signal*ret
if "pnl" not in df.columns:
    if "signal" in df.columns and "close" in df.columns:
        df["ret"] = df["close"].pct_change().fillna(0)
        df["pnl"] = df["signal"].shift(1).fillna(0) * df["ret"]
    else:
        raise SystemExit("Cannot compute pnl: missing 'pnl' column and missing 'signal'/'close'.")

# cumulative PnL time series
df["cum_pnl"] = df["pnl"].cumsum().fillna(method="ffill").fillna(0)

# daily returns series for metrics (use pnl as returns proxy here)
returns = df["pnl"].fillna(0)

def max_drawdown(ts):
    # ts: cumulative returns series
    roll_max = ts.cummax()
    dd = (ts - roll_max) / roll_max.replace(0, np.nan)
    return float(dd.min()) if not dd.dropna().empty else 0.0

metrics = {
    "total_return": float(df["cum_pnl"].iloc[-1]),
    "volatility": float(returns.std()),
    "sharpe_ratio": float((returns.mean() / returns.std()) * math.sqrt(252)) if returns.std() > 0 else 0.0,
    "max_drawdown": float(max_drawdown(df["cum_pnl"]))
}

# Save main metrics
with open(results_dir / "final_metrics.json", "w", encoding="utf8") as f:
    json.dump(metrics, f, indent=2)

# Plot cumulative PnL
plt.figure(figsize=(8,4))
plt.plot(df["cum_pnl"], label="Cumulative PnL")
plt.title("Portfolio Cumulative PnL")
plt.xlabel("Index")
plt.ylabel("Cumulative PnL")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(results_dir / "pnl_curve.png")
plt.close()

# --- Per-alpha metrics (reads any results/alpha*.csv)
per_alpha = {}
for p in sorted(results_dir.glob("alpha*.csv")):
    name = p.stem  # e.g. alpha1_meanrev
    adf = pd.read_csv(p)
    # try find pnl or compute if possible
    if "pnl" in adf.columns:
        a_series = adf["pnl"].fillna(0)
        cum = a_series.cumsum()
    elif "signal" in adf.columns and "close" in adf.columns:
        adf["ret"] = adf["close"].pct_change().fillna(0)
        adf["pnl"] = adf["signal"].shift(1).fillna(0) * adf["ret"]
        a_series = adf["pnl"].fillna(0)
        cum = a_series.cumsum()
    else:
        # fallback: skip if we can't get pnl
        per_alpha[name] = {"error": "no pnl or (signal+close) columns found"}
        continue

    rets = a_series
    per_alpha[name] = {
        "final_cum_pnl": float(cum.iloc[-1]) if not cum.empty else 0.0,
        "volatility": float(rets.std()),
        "sharpe_ratio": float((rets.mean() / rets.std()) * math.sqrt(252)) if rets.std() > 0 else 0.0,
        "max_drawdown": float(max_drawdown(cum))
    }

with open(results_dir / "per_alpha_metrics.json", "w", encoding="utf8") as f:
    json.dump(per_alpha, f, indent=2)

print("✅ Saved: results/final_metrics.json")
print("✅ Saved: results/per_alpha_metrics.json")
print("✅ Saved: results/pnl_curve.png")
