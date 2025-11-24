"""Implement the matching engine using efficient data structures
This file contains the logic for the Order Book. It uses Python's heapq module.
Sell Orders: Stored in a Min-Heap (Lowest Price first).
Buy Orders: Stored in a Max-Heap (Highest Price first). 
Since heapq is a min-heap, we store buy prices as negative values to simulate a max-heap.
"""



import heapq
from typing import List, Tuple
from decimal import Decimal
from models import Order

"""Implement the matching engine using efficient data structures (Heaps/Priority Queues) to ensure $O(\log N)$ performance for order insertion and retrieval."""

class OrderBook:
    def __init__(self, symbol: str):
        self.symbol = symbol
        # Min-Heap for Sells: (price, timestamp, order_object)
        # Python's heap pops smallest item first (Lowest Sell Price)
        self.sell_heap: List[Tuple[Decimal, str, Order]] = []
        
        # Max-Heap for Buys: (-price, timestamp, order_object)
        # We negate price so largest price pops first
        self.buy_heap: List[Tuple[Decimal, str, Order]] = []

    def process_order(self, order: Order):
        if order.side == 'buy':
            self._match_buy_order(order)
        else:
            self._match_sell_order(order)

    def _match_buy_order(self, incoming_buy: Order):
        """
        Incoming Buy tries to match against lowest resting Sells.
        """
        while incoming_buy.quantity > 0 and self.sell_heap:
            best_sell_price, _, resting_sell = self.sell_heap[0]

            # Check if match is possible (Buy Price >= Sell Price)
            if incoming_buy.price >= resting_sell.price:
                self._execute_trade(incoming_buy, resting_sell)
                
                # Cleanup: If resting sell is fully filled, remove from heap
                if resting_sell.quantity == 0:
                    heapq.heappop(self.sell_heap)
            else:
                # No overlap, stop matching
                break

        # If buy order is not fully filled, add remainder to book
        if incoming_buy.quantity > 0:
            # Push to Buy Heap: (-price, timestamp, order)
            # -price ensures Max-Heap behavior
            heapq.heappush(self.buy_heap, (-incoming_buy.price, incoming_buy.timestamp, incoming_buy))

    def _match_sell_order(self, incoming_sell: Order):
        """
        Incoming Sell tries to match against highest resting Buys.
        """
        while incoming_sell.quantity > 0 and self.buy_heap:
            # Note: price is stored as negative in buy_heap
            neg_best_buy_price, _, resting_buy = self.buy_heap[0]
            
            # Check if match is possible (Buy Price >= Sell Price)
            if resting_buy.price >= incoming_sell.price:
                self._execute_trade(resting_buy, incoming_sell)
                
                # Cleanup: If resting buy is fully filled, remove from heap
                if resting_buy.quantity == 0:
                    heapq.heappop(self.buy_heap)
            else:
                break

        # If sell order is not fully filled, add remainder to book
        if incoming_sell.quantity > 0:
            # Push to Sell Heap: (price, timestamp, order)
            heapq.heappush(self.sell_heap, (incoming_sell.price, incoming_sell.timestamp, incoming_sell))

    def _execute_trade(self, buy_order: Order, sell_order: Order):
        """
        Executes trade.
        Rule: Trade Price is ALWAYS the Sell Order's price.
        """
        match_qty = min(buy_order.quantity, sell_order.quantity)
        
        # Per requirements: Trade recorded at price of the sell order
        trade_price = sell_order.price

        # Update quantities
        buy_order.quantity -= match_qty
        sell_order.quantity -= match_qty

        # Print Output Format: <BuyOrderId> <TradePrice> <Qty> <SellOrderId>
        print(f"{buy_order.order_id} {trade_price:.2f} {match_qty} {sell_order.order_id}")