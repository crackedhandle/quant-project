import json, random, numpy as np, os
from pathlib import Path
from datetime import datetime
from data_adapter import bars_csv_to_eventstream
from alphas.alpha1_meanrev import MeanRevAlpha
from portfolio import SimplePortfolio
from execution import ExecutionSimulator

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)

def seed_everything(seed):
    random.seed(seed)
    np.random.seed(seed)

class Engine:
    def __init__(self, alphas, portfolio, execution, seed=42):
        self.alphas = alphas
        self.portfolio = portfolio
        self.execution = execution
        self.seed = seed
        seed_everything(seed)
        self.event_log = []
        self.trade_log = []

    def load_events(self, path):
        with open(path, "r", encoding="utf8") as f:
            return json.load(f)

    def run(self, events_path):
        events = self.load_events(events_path)
        for ev in events:
            self.event_log.append(ev)
            for alpha in self.alphas:
                sig = alpha.on_event(ev)
                if sig:
                    self.portfolio.on_signal(sig, ev['ts'])
            orders = self.portfolio.generate_orders(ev['ts'])
            if orders:
                fills = self.execution.execute(orders, ev)
                for f in fills:
                    self.portfolio.on_fill(f)
                    self.trade_log.append(f)
        last_price = events[-1]['payload']['c'] if events else 0
        pnl = self.portfolio.compute_pnl({"SYM1": last_price})
        ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        with open(RESULTS / f"trades_replay_{ts}.json", "w", encoding="utf8") as f:
            json.dump(self.trade_log, f, indent=2)
        with open(RESULTS / f"events_replay_{ts}.json", "w", encoding="utf8") as f:
            json.dump(self.event_log, f, indent=2)
        return {"pnl": pnl, "trades": len(self.trade_log)}

if __name__ == "__main__":
    import sys
    csv = sys.argv[1] if len(sys.argv)>1 else os.path.join("..","data","bars_1m.csv")
    bars_csv_to_eventstream(csv, out_json=os.path.join("..","data","events_local.json"))
    eng = Engine([MeanRevAlpha()], SimplePortfolio(), ExecutionSimulator(), seed=123)
    print("running engine on ..\\data\\events_local.json ...")
    r = eng.run(os.path.join("..","data","events_local.json"))
    print("result:", r)
