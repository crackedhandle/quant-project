import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Generate synthetic daily returns for now (replace later with real portfolio returns)
returns = pd.Series(np.random.normal(0.001, 0.01, 250))
cumulative = (1 + returns).cumprod() - 1
rolling_sharpe = returns.rolling(30).mean() / returns.rolling(30).std()

plt.figure(figsize=(10,5))
plt.subplot(2,1,1)
plt.plot(cumulative, label="Cumulative Return")
plt.legend()

plt.subplot(2,1,2)
plt.plot(rolling_sharpe, label="Rolling Sharpe (30d)", color="orange")
plt.legend()

os.makedirs("results", exist_ok=True)
plt.tight_layout()
plt.savefig("results/rolling_metrics.png")
print("? Saved rolling metrics chart to results/rolling_metrics.png")
