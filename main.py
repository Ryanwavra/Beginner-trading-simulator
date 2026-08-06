import logging
import trader
import strategy
import market
import orchestrator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    handlers=[
        logging.FileHandler("logs/engine.log", mode="w"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    market_data = market.MarketData()
    trader_obj = trader.Trader()
    strategy_obj = strategy.Strategy(trader_obj)
    engine = orchestrator.Orchestrator(market_data, strategy_obj, trader_obj)

    logger.info("Engine starting")

    try:
        engine.run()
        results = engine.finalize()
        print(results)
    except Exception:
        logger.critical("Engine crashed unexpectedly", exc_info=True)

    logger.info("Engine stopped")

if __name__ == "__main__":
    main()