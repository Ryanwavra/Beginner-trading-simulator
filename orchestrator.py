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
            if i % 50000 == 0:
                logger.info(f"Processed {i} candles...")

            try:
                self.strategy.update(candle)
            except Exception:
                logger.exception("Strategy failed during update() cycle")



        logger.info("Orchestrator run completed")

    def finalize(self):
        try:
            last_price = self.market.candles[-1]["close"]
            logger.info(f"Finalizing trades at last price: {last_price}")
            self.strategy.last_sell(last_price)


            return {
                'final_balance': self.trader.balance,
                'trade_history': self.trader.history,
                'open_trades': self.trader.trades
            }

        except Exception:
            logger.exception("Finalization failed")
            raise
