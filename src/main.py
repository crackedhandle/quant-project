import json
import os
from src.portfolio import run_portfolio

def main():
    results = run_portfolio()
    print("\n=== Portfolio Results ===")
    print(results)

    outdir = "results"
    os.makedirs(outdir, exist_ok=True)
    outpath = os.path.join(outdir, "results_multi.json")

    with open(outpath, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults written to {outpath}")

if __name__ == "__main__":
    main()
from src.metrics import calculate_metrics
import numpy as np
import pandas as pd

# Simulated daily returns (for now you can use total_portfolio_pnl / 100)
returns = pd.Series(np.random.normal(0.001, 0.01, 100))
metrics = calculate_metrics(returns)

print("\n=== Risk Metrics ===")
for k, v in metrics.items():
    print(f"{k}: {v:.4f}")
import json
import os

# Ensure results directory exists
os.makedirs("results", exist_ok=True)

# Save metrics to file
with open("results/metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)

print("\nMetrics saved to results/metrics.json")
