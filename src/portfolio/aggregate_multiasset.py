import os
import pandas as pd

# Collect all alpha result files
result_dir = "results"
alpha_files = [f for f in os.listdir(result_dir) if f.startswith("alpha") and f.endswith(".csv")]

dfs = []
for f in alpha_files:
    df = pd.read_csv(os.path.join(result_dir, f))
    df["alpha_name"] = f
    dfs.append(df)

# Concatenate all alpha DataFrames
combined = pd.concat(dfs, ignore_index=True)

# Compute mean signal and mean PnL across alphas
agg = combined.groupby("close", as_index=False)[["signal", "pnl"]].mean()
agg.to_csv("results/portfolio_aggregated.csv", index=False)

print("✅ Portfolio aggregation complete → results/portfolio_aggregated.csv")
