import pandas as pd
from src.utils.data_loader import load_prices
from src.utils.helpers import save_results

def alpha3_single_timeframe():
    df = load_prices()
    breakout_signal = (df["close"] > df["close"].shift(1)).astype(int)
    save_results(breakout_signal.mean(), "results/alpha3_breakout_pnl")
    return breakout_signal

if __name__ == "__main__":
    alpha3_single_timeframe()
