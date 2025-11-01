import json, glob, os
def load_latest(path_glob):
    files = sorted(glob.glob(path_glob))
    return json.load(open(files[-1], encoding="utf8")) if files else []

sandbox_path = "results\\trades_sandbox.json"
sandbox = json.load(open(sandbox_path, encoding="utf8")) if os.path.exists(sandbox_path) else []
replay = load_latest("results\\trades_replay_*.json")
sandbox_pnl = sum(t.get("price",0)*t.get("qty",0) * (1 if t.get("side")=="SELL" else -1) for t in sandbox)
replay_pnl  = sum(t.get("price",0)*t.get("qty",0) * (1 if t.get("side")=="SELL" else -1) for t in replay)
out = {
  "portfolio_pnl": {"sandbox_pnl": sandbox_pnl, "backtest_pnl": replay_pnl, "pnl_match": "PASS" if abs(sandbox_pnl-replay_pnl) < 1e-8 else "FAIL"},
  "alphas": {}
}
with open("results\\results.json","w", encoding="utf8") as f:
    json.dump(out, f, indent=2)
print("wrote results\\results.json")
