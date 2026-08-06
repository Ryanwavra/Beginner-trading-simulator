import logging
logger = logging.getLogger(__name__)

class Strategy:
    def __init__(self, trader, config):
        self.trader = trader
        self.config = config

    def buy(self, price):
        try:
            if price < self.config["buy_threshold"]:
                logger.info(f"Buy signal at {price}")
                stop_loss = price - self.config["stop_loss_offset"]
                self.trader.buy(price, stop_loss)

        except Exception:
            logger.exception("Strategy buy() failed")

    def sell(self, price):
        try:
            for trade in self.trader.trades[:]:

                # Take profit
                if price > self.config["take_profit"]:
                    logger.info(f"Sell signal (take profit) at {price}")
                    self.trader.update_trade(trade, price)

                # Stop loss
                elif price <= trade['stop_loss']:
                    logger.info(f"Sell signal (stop loss) at {price}")
                    self.trader.update_trade(trade, price)

                # Trailing stop
                elif price >= trade['stop_loss'] + self.config["trailing_offset"]:
                    logger.info(f"Trailing stop moved at {price}")
                    trade['stop_loss'] = price - self.config["stop_loss_offset"]


        except Exception:
            logger.exception("Strategy sell() failed")

    def last_sell(self, price):
        try:
            logger.info(f"Final sell at {price}")
            for trade in self.trader.trades[:]:
                self.trader.update_trade(trade, price)
        except Exception:
            logger.exception("Strategy last_sell() failed")
