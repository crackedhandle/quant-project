import json
import matplotlib.pyplot as plt
from pathlib import Path

results_path = Path("results/results_multi.json")
with open(results_path) as f:
    data = json.load(f)

plt.bar(data.keys(), data.values())
plt.title("Portfolio PnL Breakdown")
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig("results/portfolio_pnl_breakdown.png")  # save to file
print("? Saved chart to results/portfolio_pnl_breakdown.png")
