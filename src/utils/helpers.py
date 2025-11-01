import json
import os
from pathlib import Path
import pandas as pd

def _ensure_path(pathlike):
    p = Path(pathlike)
    # If path is directory or no suffix -> use default filename
    if p.exists() and p.is_dir():
        p = p / "results_multi.json"
    if p.suffix == "":
        p = p.with_suffix(".json")
    p.parent.mkdir(parents=True, exist_ok=True)
    return p

def save_results(data, filename="results/results_multi.json"):
    """
    Save `data` to filename.
    - If data is a dict -> save JSON
    - If data is a pandas Series/DataFrame -> save CSV
    - If filename is a directory or has no suffix -> a default filename is used
    Returns the full path string written.
    """
    p = _ensure_path(filename)

    # If pandas object -> save CSV for easier inspection
    if isinstance(data, (pd.Series, pd.DataFrame)):
        # If Series, convert to DataFrame with single column
        if isinstance(data, pd.Series):
            df = data.to_frame(name="value")
        else:
            df = data
        df.to_csv(p.with_suffix(".csv"), index=False)
        return str(p.with_suffix(".csv"))

    # If dict (or other), save JSON
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return str(p)
