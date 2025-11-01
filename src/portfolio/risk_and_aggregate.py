import pandas as pd
from pathlib import Path
alpha_files = sorted(Path("results").glob("alpha*_multiasset.csv")) + sorted(Path("results").glob("alpha*_single_timeframe.csv")) + sorted(Path("results").glob("alpha*.csv"))
alpha_files = [p for p in alpha_files if p.exists()]
if not alpha_files:
    print("No alpha files found in results/")
else:
    df = None
    for p in alpha_files:
        a = pd.read_csv(p)
        col = a.columns[-1]  # last numeric col (pnl or signal)
        # try to pick signal if exists
        if "signal" in a.columns:
            s = a["signal"]
        else:
            # fallback to sign of pnl diff -> crude
            s = (a.iloc[:,0].diff().fillna(0) > 0).astype(int)*2-1
        if df is None:
            df = pd.DataFrame({"signal_sum": s})
        else:
            df["signal_sum"] = df["signal_sum"].add(s, fill_value=0)
    # normalize to -1..1
    df["portfolio_signal"] = (df["signal_sum"] / df["signal_sum"].abs().max()).fillna(0)
    df["pnl"] = df["portfolio_signal"].shift(1) * df["portfolio_signal"].pct_change().fillna(0)
    df.to_csv("results/portfolio_aggregated.csv", index=False)
    print("✅ Portfolio aggregated → results/portfolio_aggregated.csv")
