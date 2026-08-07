import logging
logger = logging.getLogger(__name__)

class Trader:
    def __init__(self, config):
        self.balance = 0
        self.trades = []
        self.history = []
        self.config = config

        self.equity_curve = []

    def buy(self, position, stop_loss, timestamp):
        try:
            self.trades.append({
                'position': position,
                'stop_loss': stop_loss,
                'timestamp': timestamp
            })
            logger.info(f"Opened trade at {position} with stop loss {stop_loss}")
        except Exception:
            logger.exception("Trader buy() failed")

    def update_trade(self, trade, price):
        try:
            pnl = price - trade['position']
            logger.info(f"Closed trade at {price}, PnL={pnl}")

            self.history.append({
                'entry_price': trade['position'],
                'exit_price': price,
                'pnl': pnl,
                'timestamp': trade['timestamp']
            })

            self.balance += pnl
            self.trades.remove(trade)

            self.equity_curve.append({
                'balance':self.balance,
                'timestamp': trade['timestamp']
            })

            return trade

        except Exception:
            logger.exception("Trader update_trade() failed")
            raise
