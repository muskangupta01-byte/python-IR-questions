from dataclasses import dataclass
from decimal import Decimal

"""Define the Order class."""

@dataclass
class Order:
    order_id: str
    timestamp: str
    symbol: str
    side: str  # 'buy' or 'sell'
    price: Decimal
    quantity: int

    def __post_init__(self):
        # Ensure proper types
        self.price = Decimal(self.price)
        self.quantity = int(self.quantity)