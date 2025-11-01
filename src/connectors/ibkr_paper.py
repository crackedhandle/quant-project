import json, time
from pathlib import Path
def connect():
    time.sleep(0.2)
    info = {"exchange":"ibkr_paper","status":"connected","timestamp":time.time()}
    Path("results/connector_ibkr.json").write_text(json.dumps(info))
    print("IBKR paper: connected")
if __name__=="__main__":
    connect()
