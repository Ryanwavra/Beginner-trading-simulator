import logging
import talib
import numpy as np

logger = logging.getLogger(__name__)

class Strategy:
    def __init__(self, trader, config):
        self.trader = trader
        self.config = config

        #STore closing prices as they come in 
        self.closes = []

    def update(self, candle):
        try:
            price = candle["close"]
            self.closes.append(price)

            #We need enough candles to compute EMA_slow
            if len(self.closes) < self.config["ema_slow"]:
                return

            closes_np = np.array(self.closes)

            #compute EMAs using TA-Lib
            ema_fast = talib.EMA(closes_np, timeperiod=self.config["ema_fast"])
            ema_slow = talib.EMA(closes_np, timeperiod=self.config["ema_slow"])

            i = len(closes_np) - 1 #current index

            #Entry Logic for EMA Crossover

            #Fast EMA crosses above slow EMA = BUY
            if ema_fast[i] > ema_slow[i]:
                logger.info(f"Buy signal at {price}")
                stop_loss = price - self.config["Stop_loss_offset"]
                self.trader.buy(price, stop_loss)

            #Fast EMA crosses below slow EMA = SELL
            elif ema_fast[i] < ema_slow[i]:
                logger.info(f"Sell signal at {price}")
                for trade in self.trader.trades[:]:
                    self.trader.update_trad(trade, price)

            #Risk Management
            for trade in self.trader.trades[:]:

                #Stop loss hit
                if price <= trade['stop_loss']:
                    logger.info(f"Stop loss hit at {price}")
                    self.trader.update_trade(trade, price)

                #Trailing stop movement
                elif price >= trade['stop_loss'] + self.config['trailing_offset']:
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
