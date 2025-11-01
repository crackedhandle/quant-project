 
import pandas as pd

def run_backtest(window, threshold):
    df = pd.read_csv("data/prices.csv")
    df.columns = [c.strip().capitalize() for c in df.columns]  # Normalize column names

    df["rolling_mean"] = df["Close"].rolling(window).mean()
    df["z_score"] = (df["Close"] - df["rolling_mean"]) / df["Close"].rolling(window).std()
    df["position"] = 0
    df.loc[df["z_score"] > threshold, "position"] = -1
    df.loc[df["z_score"] < -threshold, "position"] = 1
    df["returns"] = df["Close"].pct_change()
    df["strategy"] = df["position"].shift(1) * df["returns"]
    pnl = df["strategy"].cumsum().iloc[-1]
    return pnl

