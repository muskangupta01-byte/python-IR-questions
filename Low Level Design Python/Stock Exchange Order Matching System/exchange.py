from typing import Dict
from models import Order
from order_book import OrderBook

class ExchangeEngine:
    def __init__(self):
        # Map: Symbol -> OrderBook
        self.order_books: Dict[str, OrderBook] = {}

    def process_line(self, line: str):
        if not line.strip():
            return

        # Parsing Logic
        # Input: #1 09:45 BAC sell 240.12 100
        parts = line.split()
        if len(parts) != 6:
            return

        order_id = parts[0]
        timestamp = parts[1]
        symbol = parts[2]
        side = parts[3].lower()
        price = parts[4]
        qty = parts[5]

        order = Order(order_id, timestamp, symbol, side, price, qty)

        # Get or Create Order Book for this symbol
        if symbol not in self.order_books:
            self.order_books[symbol] = OrderBook(symbol)

        self.order_books[symbol].process_order(order)