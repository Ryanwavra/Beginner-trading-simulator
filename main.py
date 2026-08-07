import json
import logging
import trader
import strategy
import market
import orchestrator

with open("config/default.json") as f:
    config = json.load(f)

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s [%(name)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/engine.log", mode="w"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    logger.info("Engine starting")
    try:
        market_data = market.MarketData(config)
        trader_obj = trader.Trader(config)
        strategy_obj = strategy.Strategy(trader_obj, config)
        engine = orchestrator.Orchestrator(market_data, strategy_obj, trader_obj, config)

        engine.run()
        results = engine.finalize()
        logger.warning(
        f"FINAL RESULTS | Balance: {results['final_balance']} | "
        f"Trades: {len(results['trade_history'])} | "
        f"Open: {len(results['open_trades'])}"
)


    except Exception:
        logger.critical("Engine crashed unexpectedly", exc_info=True)

    finally:
        logger.info("Engine stopped")

if __name__ == "__main__":
    main()