from pathlib import Path
import pandas as pd
from src.strategy.mean_reversion import mean_reversion_strategy

# Load data
prices_path = Path("data/prices.csv")

# Read best parameters (single-column CSV)
params = pd.read_csv("results/best_params.csv", header=None).iloc[:, 0]
window = int(params[0])
threshold = float(params[1])

# Run strategy
total_pnl = mean_reversion_strategy(prices_path, window, threshold)

# Save and print results
pd.DataFrame([{"window": window, "threshold": threshold, "pnl": total_pnl}]).to_csv("results/tuned_strategy_results.csv", index=False)
print(f"✅ Retested with window={window}, threshold={threshold}, pnl={total_pnl}")

