from .data_loader import load_data
import pandas as pd

def save_alpha(df, filename):
    df.to_csv(f"results/{filename}.csv", index=False)
