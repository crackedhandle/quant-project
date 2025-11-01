import json
from pathlib import Path
import pandas as pd
import numpy as np

results_dir = Path("results")
alphas = sorted(results_dir.glob("alpha*.csv"))
if not alphas:
    raise SystemExit("No alpha files found in results/. Run alpha scripts first.")

alpha_data = {}
for path in alphas:
    name = path.stem
    df = pd.read_csv(path)
    if "pnl" not in df.columns:
        if "signal" in df.columns and "close" in df.columns:
            df["ret"] = df["close"].pct_change().fillna(0)
            df["pnl"] = df["signal"].shift(1).fillna(0) * df["ret"]
        else:
            continue
    alpha_data[name] = df["pnl"].fillna(0).values

# Align all pnl series by length
max_len = max(len(v) for v in alpha_data.values())
for k,v in alpha_data.items():
    if len(v) < max_len:
        pad = np.zeros(max_len - len(v))
        alpha_data[k] = np.concatenate([v, pad])

names = list(alpha_data.keys())
returns = np.column_stack([alpha_data[n] for n in names])
mean_ret = returns.mean(axis=0)
vol = returns.std(axis=0)

# Equal weights
equal_w = np.ones(len(names)) / len(names)
# Volatility-scaled (inverse vol)
inv_vol = 1 / np.clip(vol, 1e-8, None)
vol_scaled_w = inv_vol / inv_vol.sum()

# Combine pnl
portfolio_equal = returns @ equal_w
portfolio_volscaled = returns @ vol_scaled_w

# Save weights
weights = {
    "alphas": names,
    "equal_weights": equal_w.tolist(),
    "vol_scaled_weights": vol_scaled_w.tolist()
}
with open(results_dir / "portfolio_weights.json", "w", encoding="utf8") as f:
    json.dump(weights, f, indent=2)

# Save portfolio pnl
df_out = pd.DataFrame({
    "equal": portfolio_equal,
    "vol_scaled": portfolio_volscaled
})
df_out["cum_equal"] = df_out["equal"].cumsum()
df_out["cum_vol_scaled"] = df_out["vol_scaled"].cumsum()
df_out.to_csv(results_dir / "portfolio_backtest.csv", index=False)

print("✅ Saved: results/portfolio_weights.json")
print("✅ Saved: results/portfolio_backtest.csv")
