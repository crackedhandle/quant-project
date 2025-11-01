import numpy as np
import pandas as pd

def generate_signals(df, lookback=30, z_entry=1.5, z_exit=0.5):
    # create a deterministic "asset B" from asset A (close) so we can test pair logic
    asset_a = df['close'].astype(float)
    # synthetic asset B: small deterministic transform of A (sinusoidal spread)
    asset_b = asset_a * (1 + 0.001 * np.sin(np.arange(len(asset_a))/10.0))
    spread = asset_a - asset_b
    mu = spread.rolling(window=lookback, min_periods=1).mean()
    sigma = spread.rolling(window=lookback, min_periods=1).std().replace(0, 1e-9)
    z = (spread - mu) / sigma

    sig = pd.Series(0, index=df.index)
    pos = 0
    for i in range(len(df)):
        zi = z.iat[i]
        if np.isnan(zi):
            sig.iat[i] = 0
            continue
        if pos == 0:
            if zi > z_entry:
                pos = -1   # short spread (short A / long B)
            elif zi < -z_entry:
                pos = 1    # long spread (long A / short B)
        else:
            if abs(zi) < z_exit:
                pos = 0
        sig.iat[i] = pos

    df['signal'] = sig
    df['spread'] = spread
    return df

def compute_pnl(df):
    df = df.copy()
    df['ret'] = df['close'].pct_change().fillna(0)
    # approximate spread PnL by trading asset A only with the sign (proxy)
    df['pnl'] = df['signal'].shift(1).fillna(0) * df['ret']
    return df['pnl'].cumsum().iloc[-1]
import pandas as pd, numpy as np
from src.utils.data_loader import load_data

df = load_data("data/prices.csv")
df["signal"] = np.where(df["close"].pct_change() > 0.01, 1, -1)
df["ret"] = df["close"].pct_change()
df["pnl"] = df["signal"].shift(1) * df["ret"]
df.to_csv("results/alpha4_multiasset.csv", index=False)
print("✅ Saved: results/alpha4_multiasset.csv")
