import pandas as pd

df = pd.read_csv('results/hpt_summary.csv')
best = df.loc[df['cum_pnl'].idxmax()]

print("=== Best Hyperparameters ===")
print(f"Window: {best['window']}")
print(f"Threshold: {best['threshold']}")
print(f"Cumulative PnL: {best['cum_pnl']:.4f}")

best.to_csv('results/best_params.csv', index=False)
print("\nSaved best parameters to results/best_params.csv")
