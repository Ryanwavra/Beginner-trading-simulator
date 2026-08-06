import logging
logger = logging.getLogger(__name__)

class Strategy:
    def __init__(self, trader):
        self.trader = trader

    def buy(self, price):
        try:
            if price < 100:
                logger.info(f"Buy signal at {price}")
                stop_loss = price - 25
                self.trader.buy(price, stop_loss)
        except Exception:
            logger.exception("Strategy buy() failed")

    def sell(self, price):
        try:
            for trade in self.trader.trades[:]:

                # Take profit
                if price > 200:
                    logger.info(f"Sell signal (take profit) at {price}")
                    self.trader.update_trade(trade, price)

                # Stop loss
                elif price <= trade['stop_loss']:
                    logger.info(f"Sell signal (stop loss) at {price}")
                    self.trader.update_trade(trade, price)

                # Trailing stop
                elif price >= trade['stop_loss'] + 50:
                    logger.info(f"Trailing stop moved at {price}")
                    trade['stop_loss'] = price - 25

        except Exception:
            logger.exception("Strategy sell() failed")

    def last_sell(self, price):
        try:
            logger.info(f"Final sell at {price}")
            for trade in self.trader.trades[:]:
                self.trader.update_trade(trade, price)
        except Exception:
            logger.exception("Strategy last_sell() failed")
