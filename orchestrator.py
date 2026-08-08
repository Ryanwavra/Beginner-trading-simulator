import logging
logger = logging.getLogger(__name__)

class Orchestrator:
    def __init__(self, market, strategy, trader, config):
        self.market = market
        self.strategy = strategy
        self.trader = trader
        self.config = config

    def run(self):
        logger.info("Orchestrator run started")

        for i, candle in enumerate(self.market.candles):

            # ADD THIS LINE — inject index into candle
            candle["index"] = i

            if i % 200000 == 0:
                print(f"Processed {i} candles...")

            try:
                self.strategy.update(candle)
            except Exception:
                logger.exception("Strategy failed during update() cycle")

        logger.info("Orchestrator run completed")

    def finalize(self):
        try:
            last_candle = self.market.candles[-1]
            last_price = last_candle["close"]

            # ADD THESE TWO LINES
            last_timestamp = last_candle["timestamp"]
            last_index = last_candle["index"]

            logger.info(f"Finalizing trades at last price: {last_price}")
            self.strategy.last_sell(last_price, last_timestamp, last_index)

            return {
                'final_balance': self.trader.balance,
                'trade_history': self.trader.history,
                'open_trades': self.trader.trades,
                'equity_curve': self.trader.equity_curve
            }

        except Exception:
            logger.exception("Finalization failed")
            raise
