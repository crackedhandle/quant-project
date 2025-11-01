from src.utils import load_data, save_alpha
import pandas as pd

def compute_alpha3(data: pd.DataFrame) -> pd.Series:
    return (data["close"] - data["open"]) / data["open"]

if __name__ == "__main__":
    df = load_data("data/bars_1m.csv")
    alpha3 = compute_alpha3(df)
    save_alpha(alpha3, "alpha3_single_timeframe.csv")
    print("✅ Alpha 3 computed and saved successfully.")
