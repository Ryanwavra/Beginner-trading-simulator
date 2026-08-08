import logging
logger = logging.getLogger(__name__)

class Trader:
    def __init__(self, config):
        self.balance = 0
        self.trades = []      # open trades
        self.history = []     # closed trades
        self.config = config
        self.equity_curve = []

    def buy(self, price, stop_loss, timestamp, index):
        try:
            self.trades.append({
                'entry_price': price,
                'entry_timestamp': timestamp,
                'entry_index': index,
                'stop_loss': stop_loss
            })
            logger.info(f"Opened trade at {price} with stop loss {stop_loss}")
        except Exception:
            logger.exception("Trader buy() failed")

    def update_trade(self, trade, price, timestamp, index):
        try:
            pnl = price - trade['entry_price']
            logger.info(f"Closed trade at {price}, PnL={pnl}")

            # Closed trade record
            self.history.append({
                'entry_price': trade['entry_price'],
                'exit_price': price,
                'pnl': pnl,
                'entry_timestamp': trade['entry_timestamp'],
                'exit_timestamp': timestamp,
                'entry_index': trade['entry_index'],
                'exit_index': index,
                'stop_loss': trade['stop_loss']
            })

            self.balance += pnl
            self.trades.remove(trade)

            # Equity curve
            self.equity_curve.append({
                'balance': self.balance,
                'timestamp': timestamp
            })

            return trade

        except Exception:
            logger.exception("Trader update_trade() failed")
            raise
