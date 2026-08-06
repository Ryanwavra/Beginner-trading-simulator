class Trader:
    def __init__(self):
        self.balance = 0
        self.trades = []
        self.history = []

    def buy(self, position, stop_loss):
        self.trades.append({
            'position': position,
            'stop_loss': stop_loss
        })

    def update_trade(self, trade, price):
        self.history.append(f"opened @ ${trade['position']}, closed @ {price}, profit ${price - trade['position']}")
        self.balance += price - trade['position']
        self.trades.remove(trade)
        return trade