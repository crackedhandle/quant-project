from src.utils.data_loader import load_data; import sys, numpy as np, pandas as pd
filepath = sys.argv[1] if len(sys.argv) > 1 else "data/prices.csv"
df = load_data(filepath)
df["signal"] = np.where(df["close"].rolling(3).mean() > df["close"].rolling(7).mean(), 1, -1)
df["ret"] = df["close"].pct_change()
df["pnl"] = df["signal"].shift(1) * df["ret"]
df.to_csv("results/alpha2_multiasset.csv", index=False)
print("✅ Saved: results/alpha2_multiasset.csv")
