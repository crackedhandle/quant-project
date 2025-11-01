import numpy as np

def generate_signals(df):
    df['signal'] = np.where(df['close'] > df['close'].rolling(5).mean(), 1, -1)
    return df

def compute_pnl(df):
    df['ret'] = df['close'].pct_change()
    df['pnl'] = df['signal'].shift(1) * df['ret']
    return df['pnl'].cumsum().iloc[-1]
