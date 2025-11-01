import sys
import numpy as np
import pandas as pd

# choose filepath from argv or default to data/prices.csv
filepath = sys.argv[1] if len(sys.argv) > 1 else "data/prices.csv"

# read prices (robust basic read)
df = pd.read_csv(filepath, parse_dates=True, infer_datetime_format=True)

# ensure required column exists
if "close" not in df.columns:
    raise SystemExit("ERROR: input CSV must contain a 'close' column")

# compute signals and pnl
df = df.copy()
df["signal"] = np.where(df["close"] < df["close"].rolling(5).mean(), 1, -1)
df["ret"] = df["close"].pct_change()
df["pnl"] = df["signal"].shift(1) * df["ret"]

# save full signal dataframe and also a small pnl summary
out_csv = "results/alpha1_multiasset.csv"
summary_json = "results/alpha1_multiasset_summary.json"
df.to_csv(out_csv, index=False)

import json
summary = {"final_cumulative_pnl": float(df["pnl"].cumsum().iloc[-1]) if not df["pnl"].dropna().empty else 0.0}
open(summary_json, "w", encoding="utf8").write(json.dumps(summary, indent=2))

print(f"✅ Saved: {out_csv}")
print(f"✅ Saved: {summary_json}")
