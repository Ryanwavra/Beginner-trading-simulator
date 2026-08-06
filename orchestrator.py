class Orchestrator:
    def __init__(self, market, strategy, trader):
        self.market = market
        self.strategy = strategy
        self.trader = trader
        self.prices = self.market.trend_generation()

    def run(self):
        for price in self.prices:
            self.strategy.buy(price)
            self.strategy.sell(price)

    def finalize(self):
        if self.prices:
            last_price = self.prices[-1]
            self.strategy.last_sell(last_price)

        return {
            'final_balance': self.trader.balance,
            'trade_history': self.trader.history, 
            'open_trades': self.trader.trades
        }