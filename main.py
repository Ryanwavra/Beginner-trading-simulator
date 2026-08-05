import random

trader = {
    'balance': 0,
    'trades': [],
    'trade_history': []
}

def update_trade(trade, price):
    trader['trade_history'].append(f"opened @ ${trade['position']}, closed @ ${price}, profit ${price - trade['position']}")
    trader['balance'] += price - trade['position']
    trader['trades'].remove(trade)
    return trade
    

def buy(price):
    if price < 100:
        trader['trades'].append({
            'position': price,
            'stop_loss': price - 25
        })
        return trader


def sell(price):
    for trade in trader["trades"]:

        #take profit
        if price > 200:
            update_trade(trade, price)

        #stop loss
        elif price <= trade['stop_loss']:
            update_trade(trade, price)

        #trailing stop
        elif price >= trade['stop_loss'] + 50:
            trade['stop_loss'] = price - 25


def last_sell(price):
    for trade in trader['trades'][:]:
        update_trade(trade, price)


def trend_generation():
    trend_prices = []

    #start price
    trend_prices.append(random.randint(1, 300))

    #next price logic
    for i in range(50):
        trend_prices.append(trend_prices[-1] + random.randint(-10, 10) + random.randint(-3, 4))

    return trend_prices


def orchestrator():
    
    #1. Generate a sequence of prices
    prices = trend_generation()

    #2. Loop through each price
    for price in prices:
        print(f"Price: {price}")

        #3. Run your buy and sell logic
        buy(price)
        sell(price)
    
    #Sell and log last trade
    price = prices[-1]
    last_sell(price)


    #4 print final results
    print("\nFINAL TRADER STATE:")
    print(f"Balance: {trader['balance']}")
    print("Trade History:")
    for trade in trader['trade_history']:
        print(trade)

orchestrator()