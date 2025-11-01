import numpy as np
import pandas as pd

def calculate_metrics(returns: pd.Series):
    total_return = returns.sum()
    volatility = returns.std()
    sharpe_ratio = total_return / volatility if volatility != 0 else 0
    cumulative = (1 + returns).cumprod()
    max_drawdown = (cumulative / cumulative.cummax() - 1).min()
    
    return {
        "total_return": total_return,
        "volatility": volatility,
        "sharpe_ratio": sharpe_ratio,
        "max_drawdown": max_drawdown
    }
