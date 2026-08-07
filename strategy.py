import logging
logger = logging.getLogger(__name__)

class Strategy:
    def __init__(self, trader, config):
        self.trader = trader
        self.config = config

        # Incremental EMA values
        self.ema_fast = None
        self.ema_slow = None

        # Alpha coefficients for incremental EMA
        self.alpha_fast = 2 / (config["ema_fast"] + 1)
        self.alpha_slow = 2 / (config["ema_slow"] + 1)

        # Track previous EMA relationship for true crossover detection
        self.prev_fast_above = None

    def update(self, candle):
        try:
            price = candle["close"]

            # Initialize EMAs on first candle
            if self.ema_fast is None:
                self.ema_fast = price
                self.ema_slow = price
                return

            # Incremental EMA update (O(1))
            self.ema_fast = self.ema_fast + self.alpha_fast * (price - self.ema_fast)
            self.ema_slow = self.ema_slow + self.alpha_slow * (price - self.ema_slow)

            # Determine current EMA relationship
            fast_above = self.ema_fast > self.ema_slow

            # TRUE CROSSOVER ENTRY LOGIC

            # BUY only when crossover happens AND no open trades
            if self.prev_fast_above is False and fast_above is True:
                if not self.trader.trades:
                    logger.info(f"Buy signal at {price}")
                    stop_loss = price - self.config["stop_loss_offset"]
                    self.trader.buy(price, stop_loss)

            # SELL only when crossover happens AND trades exist
            if self.prev_fast_above is True and fast_above is False:
                if self.trader.trades:
                    logger.info(f"Sell signal at {price}")
                    for trade in self.trader.trades[:]:
                        self.trader.update_trade(trade, price)

            # Update previous state
            self.prev_fast_above = fast_above

            # RISK MANAGEMENT
            for trade in self.trader.trades[:]:

                # Stop loss hit
                if price <= trade['stop_loss']:
                    logger.info(f"Stop loss hit at {price}")
                    self.trader.update_trade(trade, price)

                # Trailing stop movement
                elif price >= trade['stop_loss'] + self.config["trailing_offset"]:
                    logger.info(f"Trailing stop moved at {price}")
                    trade['stop_loss'] = price - self.config["stop_loss_offset"]

        except Exception:
            logger.exception("Strategy update() failed")

    def last_sell(self, price):
        try:
            logger.info(f"Final sell at {price}")
            for trade in self.trader.trades[:]:
                self.trader.update_trade(trade, price)
        except Exception:
            logger.exception("Strategy last_sell() failed")
