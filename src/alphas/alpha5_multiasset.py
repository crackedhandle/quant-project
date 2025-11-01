import pandas as pd, numpy as np
from src.utils.data_loader import load_data

# Load data
df = load_data('data/prices.csv')

# Compute rolling 3-day mean and generate signal
df['ma3'] = df['close'].rolling(3).mean()
df['signal'] = np.where(df['close'] > df['ma3'], 1, -1)

# Compute daily returns and PnL
df['ret'] = df['close'].pct_change()
df['pnl'] = df['signal'].shift(1) * df['ret']

# Save results
df.to_csv('results/alpha5_multiasset.csv', index=False)
print('✅ Saved: results/alpha5_multiasset.csv')
