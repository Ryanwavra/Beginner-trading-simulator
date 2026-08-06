import trader
import strategy
import market
import orchestrator

market = market.MarketData()
trader = trader.Trader()
strategy = strategy.Strategy(trader)
engine = orchestrator.Orchestrator(market, strategy, trader)

engine.run()
results = engine.finalize()
print(results)
