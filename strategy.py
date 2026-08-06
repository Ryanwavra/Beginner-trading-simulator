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