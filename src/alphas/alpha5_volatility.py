import pandas as pd
from src.utils.data_loader import load_prices
from src.utils.helpers import save_results

def alpha5_multi_timeframe():
    df = load_prices()
    df["volatility"] = df["close"].pct_change().rolling(3).std()
    df["signal"] = (df["volatility"] > df["volatility"].rolling(5).mean()).astype(int)
    save_results(df, "results/alpha5_multi_timeframe.csv")
    return df

if __name__ == "__main__":
    alpha5_multi_timeframe()
