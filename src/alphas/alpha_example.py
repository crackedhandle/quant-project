import sys, pandas as pd, numpy as np
from pathlib import Path
# optional: accept data file path as arg
filepath = sys.argv[1] if len(sys.argv)>1 else "data/prices.csv"
df = pd.read_csv(filepath)
# simple signal: compare to previous close
df["signal"] = (df["Close"].diff() > 0).astype(int)*2-1
df["ret"] = df["Close"].pct_change()
df["pnl"] = df["signal"].shift(1) * df["ret"]
out = Path("results/alpha_example.csv")
df.to_csv(out, index=False)
print("✅ Saved:", out)
