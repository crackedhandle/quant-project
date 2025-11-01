import pandas as pd
import numpy as np
import os
from src.utils.helpers import save_results

def backtest_portfolio():
    # Load all alpha signals
    alpha_files = [f for f in os.listdir("results") if f.startswith("alpha") and f.endswith(".csv")]
    alphas = [pd.read_csv(f"results/{f}") for f in alpha_files]
    df = pd.concat(alphas, axis=1)

    # Ensure numeric columns only
    df = df.apply(pd.to_numeric, errors="coerce")

    # Create equal-weighted portfolio of alphas
    df["portfolio_signal"] = df.mean(axis=1)

    # Simulate random price changes (you'll replace this with real returns later)
    np.random.seed(42)
    returns = np.random.randn(len(df)) / 100  # ~1% daily volatility

    # Compute PnL
    df["pnl"] = df["portfolio_signal"].shift(1) * returns
    cumulative_pnl = df["pnl"].cumsum()

    # Save and return
    df.to_csv("results/portfolio_backtest.csv", index=False)
    save_results({"final_pnl": cumulative_pnl.iloc[-1]}, "results/portfolio_summary")
    print("✅ Backtest complete. Saved portfolio_backtest.csv and portfolio_summary.json")

if __name__ == "__main__":
    backtest_portfolio()
