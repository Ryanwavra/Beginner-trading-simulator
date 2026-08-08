import csv

class MarketData:
    def __init__(self, config):
        self.config = config
        self.candles = self.load_csv("data/nq_1min_2022-25.csv")  

    def load_csv(self, path):
        candles = []
        with open(path, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                candles.append({
                    "timestamp": str(row["timestamp ET"]),  
                    "open": float(row["open"]),
                    "high": float(row["high"]),
                    "low": float(row["low"]),
                    "close": float(row["close"]),
                    "volume": float(row["volume"])
                })
        return candles
