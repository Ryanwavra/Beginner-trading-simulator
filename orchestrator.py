import logging
logger = logging.getLogger(__name__)

class Orchestrator:
    def __init__(self, market, strategy, trader, config):
        self.market = market
        self.strategy = strategy
        self.trader = trader
        self.config = config

        self.prices = self.market.trend_generation()

    def run(self):
        logger.info("Orchestrator run started")

        for price in self.prices[:self.config["ticks"]]:
            logger.debug(f"Engine loop iteration, price={price}")
            candle = {"close", price}

            # If price is None or invalid
            if price is None:
                logger.warning("Price feed returned None")
                continue

            # Strategy decisions
            try:
                self.strategy.update(candle)
            except Exception:
                logger.exception("Strategy failed during buy/sell cycle")

        logger.info("Orchestrator run completed")

    def finalize(self):
        try:
            if self.prices:
                last_price = self.prices[-1]
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
