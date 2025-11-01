class ExecutionSimulator:
    def __init__(self, slippage_perc=0.0005):
        self.slippage_perc = slippage_perc

    def execute(self, orders, event):
        fills = []
        price = event.get("payload", {}).get("c", None)
        if price is None:
            price = orders[0].get("limit_price", 0) if orders else 0
        for o in orders:
            adj = price * (1 + (self.slippage_perc if o["side"]=="BUY" else -self.slippage_perc))
            fill = {"ts": event["ts"], "order_id": o["id"], "symbol": o["symbol"], "side": o["side"], "qty": o["qty"], "price": round(adj, 8), "fill_type":"sim"}
            fills.append(fill)
        return fills
