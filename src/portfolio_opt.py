import pandas as pd
import numpy as np
from scipy.optimize import minimize
from src.utils.helpers import save_results

def optimize_portfolio():
    # Load alpha correlation matrix
    corr = pd.read_csv("results/alpha_correlation.csv", index_col=0)
    
    # Assume expected returns based on previous alphas (toy example)
    expected_returns = pd.Series({
        "alpha1_meanrev": -0.003,
        "alpha2_momentum": -0.002,
        "alpha3_single_timeframe": 0.001,
        "alpha5_multi_timeframe": -0.0005,
    })
    
    # Convert correlation matrix to covariance (for optimization)
    cov = corr.cov()
    
    def portfolio_metrics(weights):
        port_return = np.dot(weights, expected_returns)
        port_vol = np.sqrt(np.dot(weights.T, np.dot(cov, weights)))
        sharpe = port_return / port_vol
        return -sharpe  # minimize negative Sharpe ratio

    n = len(expected_returns)
    bounds = tuple((0, 1) for _ in range(n))
    constraints = {"type": "eq", "fun": lambda w: np.sum(w) - 1}
    
    initial_weights = np.ones(n) / n
    optimized = minimize(portfolio_metrics, initial_weights,
                         method="SLSQP", bounds=bounds, constraints=constraints)

    opt_weights = pd.Series(optimized.x, index=expected_returns.index)
    save_results(opt_weights.to_dict(), "results/optimized_portfolio")
    print("✅ Portfolio optimized. Saved to results/optimized_portfolio.json")

if __name__ == "__main__":
    optimize_portfolio()
