import pandas as pd
from src.strategy.backtest import run_backtest

def optimize_params():
    best_pnl = float('-inf')
    best_params = None
    results = []

    for window in [5, 10, 15]:
        for threshold in [0.001, 0.005, 0.01]:
            pnl = run_backtest(window=window, threshold=threshold)
            results.append((window, threshold, pnl))
            print(f"✅ Tested window={window}, threshold={threshold}, pnl={pnl:.2f}")

            if pnl > best_pnl:
                best_pnl = pnl
                best_params = (window, threshold)

    df = pd.DataFrame(results, columns=["window", "threshold", "pnl"])
    df.to_csv("data/opt_results.csv", index=False)

    with open("data/best_params.csv", "w") as f:
        f.write(f"{best_params[0]},{best_params[1]},{best_pnl}")

    print(f"\n🏁 Best params found: window={best_params[0]}, threshold={best_params[1]}, pnl={best_pnl:.2f}")

if __name__ == "__main__":
    optimize_params()
