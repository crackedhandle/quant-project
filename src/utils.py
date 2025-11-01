import pandas as pd
import os

def load_data(filepath: str) -> pd.DataFrame:
    """Load CSV data into a DataFrame."""
    return pd.read_csv(filepath)

def save_alpha(alpha_series: pd.Series, filename: str):
    """Save computed alpha Series to the results directory."""
    os.makedirs("results", exist_ok=True)
    filepath = os.path.join("results", filename)
    alpha_series.to_csv(filepath, index=False)
    print(f"✅ Saved: {filepath}")
