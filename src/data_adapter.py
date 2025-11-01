import pandas as pd
import json
import os

def bars_csv_to_eventstream(csv_path, out_json=os.path.join("..","data","events_local.json")):
    df = pd.read_csv(csv_path, parse_dates=['timestamp'])
    df = df.sort_values('timestamp').reset_index(drop=True)
    events = []
    for _, r in df.iterrows():
        ev = {
            "ts": r['timestamp'].isoformat(),
            "type": "bar",
            "symbol": "SYM1",
            "payload": {"o": float(r['open']), "h": float(r['high']), "l": float(r['low']), "c": float(r['close']), "v": float(r['volume'])}
        }
        events.append(ev)
    os.makedirs(os.path.dirname(out_json), exist_ok=True)
    with open(out_json, "w", encoding="utf8") as f:
        json.dump(events, f, indent=2)
    print("wrote", out_json, "events:", len(events))
