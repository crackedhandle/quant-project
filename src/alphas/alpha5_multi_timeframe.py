from src.utils import load_data, save_alpha
import pandas as pd

def compute_alpha5(data: pd.DataFrame) -> pd.Series:
    short = data["close"].rolling(5).mean()
    long = data["close"].rolling(20).mean()
    return short - long

if __name__ == "__main__":
    df = load_data("data/bars_1m.csv")
    alpha5 = compute_alpha5(df)
    save_alpha(alpha5, "alpha5_multi_timeframe.csv")
    print("✅ Alpha 5 computed and saved successfully.")
