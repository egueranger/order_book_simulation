import heapq
import matplotlib.pyplot as plt
import numpy as np

buy_orders = []
sell_orders = []
cancelled_orders = set()

def evolve():
    global buy_orders, sell_orders, cancelled_orders
    while buy_orders and buy_orders[0][2] in cancelled_orders:
        heapq.heappop(buy_orders)
    while sell_orders and sell_orders[0][2] in cancelled_orders:
        heapq.heappop(sell_orders)
    condition = buy_orders and sell_orders and -buy_orders[0][0]>=sell_orders[0][0]
    while condition:
        best_buy_order = buy_orders[0]
        best_sell_order = sell_orders[0]
        if best_buy_order[3]<best_sell_order[3]:
            traded_qty = best_buy_order[3]
            sell_orders[0] = (best_sell_order[0], best_sell_order[1], best_sell_order[2], best_sell_order[3]-traded_qty)
            heapq.heappop(buy_orders)
        elif best_buy_order[3]>best_sell_order[3]:
            traded_qty = best_sell_order[3]
            buy_orders[0] = (best_buy_order[0], best_buy_order[1], best_buy_order[2], best_buy_order[3]-traded_qty)
            heapq.heappop(sell_orders)
        else:
            traded_qty = best_sell_order[3]
            heapq.heappop(buy_orders)
            heapq.heappop(sell_orders)
        while buy_orders and buy_orders[0][2] in cancelled_orders:
            heapq.heappop(buy_orders)
        while sell_orders and sell_orders[0][2] in cancelled_orders:
            heapq.heappop(sell_orders)
        condition = buy_orders and sell_orders and -buy_orders[0][0]>=sell_orders[0][0]

def add_order(type, price, timestamp, order_id, qty):
    global buy_orders, sell_orders, cancelled_orders
    if type=='buy':
        heapq.heappush(buy_orders, (-price, timestamp, order_id, qty))
    else:
        assert type=='sell'
        heapq.heappush(sell_orders, (price, timestamp, order_id, qty))
    evolve()

def cancel_order(id):
    global cancelled_orders
    cancelled_orders.add(id)

def modify_order(type, price, timestamp, order_id, new_id, qty):
    global buy_orders, sell_orders, cancelled_orders
    cancel_order(order_id)
    add_order(type, price, timestamp, new_id, qty)
    evolve()

T = 1000
mean = 100
sigma = 1

mid_prices = []
for t in range(1, T+1):
    type = np.random.choice(['buy', 'sell'])
    price = np.random.normal(mean, sigma)
    timestamp = t
    order_id = t
    qty = np.random.poisson(100)
    add_order(type, price, timestamp, order_id, qty)
    if buy_orders and sell_orders:
        mid_prices.append((-buy_orders[0][0]+sell_orders[0][0])/2)
    elif mid_prices:
        mid_prices.append(mid_prices[-1]) # Last known mid price
    else:
        mid_prices.append(np.nan)         # NaN otherwise, only before both order types being sent
plt.plot(np.linspace(1, T, T), mid_prices, c='red')
plt.show()