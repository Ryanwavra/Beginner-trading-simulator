import random

class MarketData:
    def __init__(self):
        self.trend_prices = []

    def trend_generation(self):
        self.trend_prices.append(random.randint(1, 300))  #start price

        for i in range(random.randint(1, 200)):
            self.trend_prices.append(self.trend_prices[-1] + random.randint(-30, 30) + random.randint(-3, 4))

        return self.trend_prices