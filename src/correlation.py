import pandas as pd

def compute_alpha_correlation():
    alpha1 = pd.read_csv("results/alpha1_meanrev.csv")
    alpha2 = pd.read_csv("results/alpha2_momentum.csv")
    alpha3 = pd.read_csv("results/alpha3_single_timeframe.csv")
    alpha5 = pd.read_csv("results/alpha5_multi_timeframe.csv")

    df = pd.concat([alpha1, alpha2, alpha3, alpha5], axis=1)
    corr = df.corr()
    corr.to_csv("results/alpha_correlation.csv", index=True)
    print("✅ Saved: results/alpha_correlation.csv")

if __name__ == "__main__":
    compute_alpha_correlation()
