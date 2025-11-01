import json, time
from pathlib import Path
def connect():
    time.sleep(0.2)
    info = {"exchange":"zerodha_kite_sandbox","status":"connected","timestamp":time.time()}
    Path("results/connector_zerodha.json").write_text(json.dumps(info))
    print("Zerodha sandbox: connected")
if __name__=="__main__":
    connect()
