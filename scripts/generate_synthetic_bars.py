import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

n = 600  # 600 minutes (~10 hours)
start = datetime.utcnow().replace(second=0, microsecond=0) - timedelta(minutes=n)
ts = [start + timedelta(minutes=i) for i in range(n)]
price = 100 + np.cumsum(np.random.default_rng(42).normal(0, 0.1, size=n))  # deterministic seed
df = pd.DataFrame({"timestamp": ts, "open": price, "high": price+0.05, "low": price-0.05, "close": price, "volume": 100 + (np.arange(n)%10)})
os.makedirs("data", exist_ok=True)
df.to_csv("data/bars_1m.csv", index=False)
print("wrote data/bars_1m.csv", len(df), "rows")
