import itertools
import pandas as pd, numpy as np
from src.utils.data_loader import load_data
from pathlib import Path

df = load_data("data/prices.csv")

# Parameter grid
windows = [3,5,10]
thresholds = [0.005, 0.01, 0.02]

results = []
for w, t in itertools.product(windows, thresholds):
    df["signal"] = np.where(df["close"] > df["close"].rolling(w).mean()*(1+t), 1, -1)
    df["ret"] = df["close"].pct_change()
    df["pnl"] = df["signal"].shift(1) * df["ret"]
    cum_pnl = df["pnl"].cumsum().iloc[-1]
    results.append({"window": w, "threshold": t, "cum_pnl": cum_pnl})

out = pd.DataFrame(results).sort_values("cum_pnl", ascending=False)
out.to_csv("results/hpt_summary.csv", index=False)
print("✅ HPT complete → results/hpt_summary.csv")
print(out.head())
