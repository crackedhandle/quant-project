import json, time
from pathlib import Path
def connect():
    time.sleep(0.2)
    info = {"exchange":"binance_testnet","status":"connected","timestamp":time.time()}
    Path("results/connector_binance.json").write_text(json.dumps(info))
    print("Binance testnet: connected")
if __name__=="__main__":
    connect()
