import pandas as pd
from pathlib import Path

def load_data(filepath="data/prices.csv"):
    p = Path(filepath)
    if not p.exists():
        raise FileNotFoundError(f"Missing file: {filepath}")
    # read CSV; if first column is a date index, use it, otherwise just read normally
    try:
        df = pd.read_csv(p, index_col=0, parse_dates=True)
    except Exception:
        df = pd.read_csv(p)
    return df
