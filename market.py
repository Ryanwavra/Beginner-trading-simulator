import logging
import random

logger = logging.getLogger(__name__)

class MarketData:
    def __init__(self):
        self.trend_prices = []

    def trend_generation(self):
        try:
            # Generate starting price
            start_price = random.randint(1, 300)
            self.trend_prices.append(start_price)
            logger.debug(f"Starting price generated: {start_price}")

            # Generate trend
            for i in range(random.randint(1, 200)):
                new_price = (
                    self.trend_prices[-1]
                    + random.randint(-30, 30)
                    + random.randint(-3, 4)
                )
                self.trend_prices.append(new_price)

            logger.debug(f"Trend generation complete. Total prices: {len(self.trend_prices)}")
            return self.trend_prices

        except Exception:
            logger.exception("Market failed to generate trend")
            raise
