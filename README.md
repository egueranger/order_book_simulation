# order_book_simulation
A limit order book implementation in Python, built to simulate zero-intelligence market microstructure dynamics.

An example of chart obtained with one simulation is order_book.png. We can see a huge difference of volatility at the beginning when the order book is empty and the lack of liquidity conveys to price jumps. The volatility decreases immediatly afterwards.

## Features

- **Price-Time Priority (FIFO):** Implements standard exchange matching logic where resting orders are prioritized by price and arrival timestamp.
- **Efficient Heap-Based Architecture:** Uses `heapq` (Min-Heap for Asks, modified Max-Heap via inverted prices for Bids) to achieve $O(\log N)$ insertions and best-price lookups.
- **Lazy Deletion ($O(1)$ Cancellations):** Avoids costly in-heap removals by tracking cancelled `order_id`s in a hash set and lazily purging them upon reaching the top of the heap.
- **Modular Design (`evolve` loop):** Decouples order ingestion from the matching loop, maintaining full symmetry between buy and sell sides and supporting dynamic order modifications.

---

## Architecture & Code Structure

```python
import heapq

buy_orders = []                # Stored as (-price, timestamp, order_id, qty)
sell_orders = []               # Stored as (price, timestamp, order_id, qty)
cancelled_orders = set()       # Stored as order_id
