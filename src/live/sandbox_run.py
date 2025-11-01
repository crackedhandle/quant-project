import pandas as pd
from pathlib import Path

# === SANDBOX SIMULATION ===
# This simulates "live" trading using your optimized parameters
# It replays data from data/prices.csv and logs each trade into results/sandbox_trades.csv

DATA = Path("data/prices.csv")
RESULTS = Path("results/sandbox_trades.csv")

if not DATA.exists():
    raise SystemExit("Missing data/prices.csv")

# Load market data
df = pd.read_csv(DATA)
if "Close" not in df.columns:
    raise SystemExit("data/prices.csv must contain a 'Close' column")

# Load best parameters
best = pd.read_csv("results/best_params.csv", header=None).squeeze()
window = int(best.iloc[0])
threshold = float(best.iloc[1])

# Initialize columns for live simulation
balance = 0.0
position = 0  # 1 = long, -1 = short, 0 = flat
logs = []

# Simulate candle-by-candle
for i in range(window, len(df)):
    window_mean = df["Close"].iloc[i - window:i].mean()
    price = df["Close"].iloc[i]

    # Generate signals
    if price > window_mean * (1 + threshold):
        position = 1   # go long
    elif price < window_mean * (1 - threshold):
        position = -1  # go short

    # PnL = position * price change
    if i > 0:
        pnl = position * (df["Close"].iloc[i] - df["Close"].iloc[i - 1])
    else:
        pnl = 0

    balance += pnl
    logs.append({
        "timestamp": df["date"].iloc[i],
        "price": price,
        "signal": position,
        "pnl": pnl,
        "balance": balance
    })

# Save logs
pd.DataFrame(logs).to_csv(RESULTS, index=False)
print(f"✅ Sandbox run complete → {RESULTS}")
