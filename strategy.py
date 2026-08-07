import logging
import talib
import numpy as np

logger = logging.getLogger(__name__)

class Strategy:
    def __init__(self, trader, config):
        self.trader = trader
        self.config = config

        # Store closing prices
        self.closes = []

        # Track previous EMA relationship for true crossover detection
        self.prev_fast_above = None

    def update(self, candle):
        try:
            price = candle["close"]
            self.closes.append(price)

            # Need enough candles to compute EMAs
            if len(self.closes) < self.config["ema_slow"]:
                return

            closes_np = np.array(self.closes)

            ema_fast = talib.EMA(closes_np, timeperiod=self.config["ema_fast"])
            ema_slow = talib.EMA(closes_np, timeperiod=self.config["ema_slow"])

            i = len(closes_np) - 1

            fast_above = ema_fast[i] > ema_slow[i]

            
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
