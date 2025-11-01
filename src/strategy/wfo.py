import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Read portfolio backtest (expects a "pnl" column: per-step PnL)
p = Path("results/portfolio_backtest.csv")
if not p.exists():
    raise SystemExit("Missing results/portfolio_backtest.csv")

df = pd.read_csv(p)
if "pnl" not in df.columns:
    raise SystemExit("portfolio_backtest.csv must contain a 'pnl' column (per-step PnL)")

n = len(df)
# default IS/OOS sizes: 60% IS, 20% OOS, step = OOS length (rolling walk-forward)
is_len = max(2, int(n * 0.6))
oos_len = max(1, int(n * 0.2))
step = oos_len

is_curves = []
oos_curves = []
fold = 0
start = 0
while start + is_len + oos_len <= n:
    is_df = df.iloc[start:start+is_len]
    oos_df = df.iloc[start+is_len:start+is_len+oos_len]

    is_eq = (1 + is_df["pnl"]).cumprod().reset_index(drop=True)
    oos_eq = (1 + oos_df["pnl"]).cumprod().reset_index(drop=True)

    is_curves.append(is_eq)
    oos_curves.append(oos_eq)
    fold += 1
    start += step

# Save all fold curves to CSV (columns: is_0,is_1,..., oos_0,oos_1,...)
out = pd.DataFrame()
for i, s in enumerate(is_curves):
    out[f"is_{i}"] = s
for i, s in enumerate(oos_curves):
    out[f"oos_{i}"] = s
out.to_csv("results/wfo_in_vs_oos.csv", index=False)

# Plot first fold (if exists)
if len(is_curves) > 0:
    plt.figure(figsize=(8,4))
    plt.plot(is_curves[0], label="IS fold 0")
    plt.plot(range(len(is_curves[0]), len(is_curves[0])+len(oos_curves[0])), oos_curves[0], label="OOS fold 0")
    plt.title("WFO: In-Sample vs Out-of-Sample (fold 0)")
    plt.xlabel("Step")
    plt.ylabel("Equity (cumprod)")
    plt.legend()
    plt.tight_layout()
    plt.savefig("results/wfo_is_vs_oos.png")
    print("✅ WFO done → results/wfo_in_vs_oos.csv and results/wfo_is_vs_oos.png")
else:
    print("⚠️ Not enough data for any WFO fold.")
