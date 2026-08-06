import random

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


class Strategy:
    def __init__(self, trader):
        self.trader = trader

    def buy(self, price):
        if price < 100:
            stop_loss = price - 25
            self.trader.buy(price, stop_loss)

    def sell(self, price):
        for trade in self.trader.trades[:]:

            #take profit
            if price > 200:
                self.trader.update_trade(trade, price)

            #Stop loss
            elif price <= trade['stop_loss']:
                self.trader.update_trade(trade, price)

            #Trailing stop
            elif price >= trade['stop_loss'] + 50:
                trade['stop_loss'] = price - 25

    def last_sell(self, price):
        for trade in self.trader.trades[:]:
            self.trader.update_trade(trade, price)


class MarketData:
    def __init__(self):
        self.trend_prices = []

    def trend_generation(self):
        self.trend_prices.append(random.randint(1, 300))  #start price

        for i in range(random.randint(1, 200)):
            self.trend_prices.append(self.trend_prices[-1] + random.randint(-30, 30) + random.randint(-3, 4))

        return self.trend_prices


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


market = MarketData()
trader = Trader()
strategy = Strategy(trader)
engine = Orchestrator(market, strategy, trader)

engine.run()
results = engine.finalize()
print(results)
