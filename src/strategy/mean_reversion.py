from pathlib import Path
import pandas as pd

def mean_reversion_strategy(prices_path, window=5, threshold=0.02):
    df = pd.read_csv(prices_path)
    df = df.copy()

    df["rolling_mean"] = df["close"].rolling(window=window).mean()
    df["rolling_std"] = df["close"].rolling(window=window).std()
    df["zscore"] = (df["close"] - df["rolling_mean"]) / df["rolling_std"]

    df["position"] = 0
    df.loc[df["zscore"] > threshold, "position"] = -1
    df.loc[df["zscore"] < -threshold, "position"] = 1

    df["pnl"] = df["position"].shift(1) * df["close"].pct_change()
    df["cumulative_pnl"] = (1 + df["pnl"]).cumprod()

    total_pnl = df["cumulative_pnl"].iloc[-1] - 1
    return total_pnl

