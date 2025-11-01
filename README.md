# Quant Project — Multi-Asset, Multi-Timeframe Portfolio System 🚀

**Short description**
A lightweight, modular quantitative trading research scaffold for multi-asset, multi-timeframe strategies. Provides a clean project layout for data ingestion, alpha models, portfolio construction, backtesting, and result export.

---

## Project layout

```
quant-project/
│
├── src/                     # Core Python source files
│   ├── data_loader.py       # Loads and preprocesses data
│   ├── alpha_models/        # Folder for alpha strategy modules
│   ├── portfolio.py         # Portfolio construction logic
│   ├── backtest.py          # Backtesting engine (entry point)
│   └── utils.py             # Helper functions
│
├── data/                    # Input datasets (CSV, OHLCV, features)
│
├── results/                 # Output results, logs, and metrics
│
├── results.json             # Final test outputs (P&L, match checks)
│
├── requirements.txt         # Python dependencies
└── README.md                # You are here
```

---

## Quickstart (Windows / PowerShell)

Copy these exact commands into PowerShell (recommended) to reproduce the environment used for development.

```powershell
# clone repo 
git clone https://github.com/crackedhandle/quant-project
cd quant-project


python -m venv .venv
.\.venv\Scripts\Activate.ps1

# update pip and install deps
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Run a quick backtest (example — adapt CLI flags as your backtest implementation requires):

```powershell

python -m src.backtest

python -m src.backtest --data data/sample_ohlcv.csv --out results/results.json
```

---

## Minimal expected `results.json` format

```json
{
  "strategy": "example_alpha",
  "start_date": "2024-01-01",
  "end_date": "2024-12-31",
  "pnl": 12345.67,
  "returns": [0.01, -0.005, 0.02],
  "metrics": {
    "sharpe": 1.2,
    "max_drawdown": 0.08
  }
}
```

---

## File skeletons 

### `src/data_loader.py` (small starter)

```python
import pandas as pd
from pathlib import Path

def load_ohlcv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["datetime"]).sort_values("datetime")
    # minimal checks
    required_cols = {"datetime", "open", "high", "low", "close", "volume"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"Missing cols: {required_cols - set(df.columns)}")
    return df

```

### `src/portfolio.py` 

```python
from typing import Dict

def simple_equal_weight(positions: Dict[str, float]) -> Dict[str, float]:
    # positions: symbol -> score
    n = len(positions)
    if n == 0:
        return {}
    weight = 1.0 / n
    return {s: weight for s in positions}
```

---

## Development notes & conventions

* Use `src/` as a package (add `__init__.py` if you need package imports).
* Keep I/O isolated: `data_loader.py` handles reads, `backtest.py` orchestrates strategy/portfolio, `results/` stores outputs.
* Pin dependencies in `requirements.txt` for reproducibility.
* Add unit tests under `tests/` and a simple `pytest` workflow if you plan CI.

---

## Contributing

1. Fork and make a feature branch.
2. Add tests for new code.
3. Open a PR and describe the change and expected behavior.

---

## License & Contact

Add your preferred license (MIT/Apache-2.0). For questions: `divyansh.shah.ece23@itbhu.ac.in`.

---

