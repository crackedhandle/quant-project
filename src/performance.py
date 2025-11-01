import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

def compute_metrics():
    df = pd.read_csv("results/portfolio_backtest.csv")
    df["cumulative"] = df["pnl"].cumsum()

    sharpe = df["pnl"].mean() / df["pnl"].std() * np.sqrt(252)
    max_drawdown = (df["cumulative"].cummax() - df["cumulative"]).max()

    metrics = {
        "sharpe_ratio": sharpe,
        "max_drawdown": max_drawdown
    }

    with open("results/portfolio_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    print("✅ Saved: results/portfolio_metrics.json")
    print(json.dumps(metrics, indent=2))

    # Plot comparison of cumulative returns from all alphas
    alpha_files = [
        "results/alpha1_meanrev.csv",
        "results/alpha2_momentum.csv",
        "results/alpha3_single_timeframe.csv",
        "results/alpha5_multi_timeframe.csv"
    ]
    plt.figure(figsize=(8,5))
    for file in alpha_files:
        name = file.split("/")[-1].replace(".csv", "")
        df_alpha = pd.read_csv(file)
        plt.plot(df_alpha.cumsum(), label=name)
    plt.title("Cumulative Returns: Individual Alphas")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    compute_metrics()
