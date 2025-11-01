import json
import importlib
import pandas as pd
import os

def run_portfolio():
    data_path = os.path.join("data", "bars_1m.csv")
    df = pd.read_csv(data_path)
    alphas = [
        "alpha1_meanrev",
        "alpha2_momentum",
        "alpha3_breakout",
        "alpha4_multiasset",
        "alpha5_volatility"
    ]

    results = {}
    signals_df = pd.DataFrame(index=df.index)  # collect signals for correlation check
    for alpha_name in alphas:
        try:
            module = importlib.import_module(f"src.alphas.{alpha_name}")
            df_alpha = module.generate_signals(df.copy())
            pnl = module.compute_pnl(df_alpha)
            results[f"{alpha_name}_pnl"] = pnl
            # store signals (aligned)
            signals_df[alpha_name] = df_alpha['signal'].fillna(0).astype(float).reset_index(drop=True)
        except Exception as e:
            results[f"{alpha_name}_error"] = str(e)

    total_pnl = sum(v for k,v in results.items() if isinstance(v, (int,float)))
    results["total_portfolio_pnl"] = total_pnl

    # save signals snapshot for later analysis
    out_signals = os.path.join("results", "signals_snapshot.csv")
    signals_df.to_csv(out_signals, index=False)
    results["_signals_csv"] = out_signals

    return results
