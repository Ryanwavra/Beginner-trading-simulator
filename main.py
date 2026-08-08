import json
import logging
import trader
import strategy
import market
import orchestrator
from argparse import ArgumentParser
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

def build_cli():
    parser = ArgumentParser(description="Trading Engine CLI")

    parser.add_argument('--sl', type=int, default=None, help='Override stop loss')
    parser.add_argument('--sl_trailing', type=int, default=None, help='Override trailing stop loss')
    parser.add_argument('--ema_fast', type=int, default=None, help='Override fast EMA')
    parser.add_argument('--ema_slow', type=int, default=None, help='Override slow EMA')
    parser.add_argument('--verbose', action="store_true", help='Enable verbose logging')

    return parser.parse_args()
    
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
    args = build_cli()

    # Apply CLI overrids to config
    if args.sl is not None:
        config['strategy']['stop_loss_offset'] = args.sl

    if args.sl_trailing is not None:
        config['strategy']['trailing_offset'] = args.sl_trailing

    if args.ema_fast is not None:
        config['strategy']['ema_fast'] = args.ema_fast

    if args.ema_slow is not None:
        config['strategy']["ema_slow"] = args.ema_slow

    if args.verbose:
        logger.setLevel(logging.INFO)

    logger.info("Engine starting")
    
    try:
        #Build engine objects using updated config
        market_data = market.MarketData(config)
        trader_obj = trader.Trader(config)
        strategy_obj = strategy.Strategy(trader_obj, config)
        engine = orchestrator.Orchestrator(market_data, strategy_obj, trader_obj, config)

        #Run the engine
        engine.run()
        results = engine.finalize()

        #Log final results
        logger.warning(
        f"FINAL RESULTS | Balance: {results['final_balance']} | "
        f"Trades: {len(results['trade_history'])} | "
        f"Open: {len(results['open_trades'])}")

        #Equity Curve Plot
        equity_curve = results["equity_curve"]

        #Extract timestamps and balances
        timestamps = [point['timestamp'] for point in equity_curve]
        balances = [point['balance'] for point in equity_curve]

        #Conver timestamps to datetime objects
        timestamps = [
            datetime.strptime(ts, "%m/%d/%Y %H:%M")
            for ts in timestamps
        ]


        plt.plot(timestamps, balances)
        plt.title("Equity Curve")
        plt.xlabel("Time")
        plt.ylabel("Balance")

        #Format X-axis dates
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3)) #quarterly tick
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


    except Exception:
        logger.critical("Engine crashed unexpectedly", exc_info=True)

    finally:
        logger.info("Engine stopped")


    

if __name__ == "__main__":
    main()