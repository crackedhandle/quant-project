import json
import pandas as pd
import matplotlib.pyplot as plt

# Load optimized weights
with open("results/optimized_portfolio.json", "r") as f:
    weights = json.load(f)

# Load all alpha PnLs
alphas = ["alpha1_meanrev", "alpha2_momentum", "alpha3_single_timeframe", "alpha4_multiasset", "alpha5_multi_timeframe"]
df = pd.DataFrame()
for a in alphas:
    df[a] = pd.read_csv(f"results/{a}.csv").iloc[:, -1]

# Weighted portfolio PnL
df["optimized_portfolio"] = sum(weights[a] * df[a] for a in alphas)
df["optimized_cum_pnl"] = df["optimized_portfolio"].cumsum()

# Save results
df.to_csv("results/final_optimized_backtest.csv", index=False)

# Plot performance
plt.plot(df["optimized_cum_pnl"], label="Optimized Portfolio")
plt.title("Final Optimized Portfolio Performance")
plt.xlabel("Time")
plt.ylabel("Cumulative PnL")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("results/final_optimized_performance.png")
plt.show()
