from collections import defaultdict
from typing import List, Set, Dict

class Seller:
    """Defines the Seller entity and manages the data 
    internal to a seller (inventory, pincodes, payment modes)."""
    def __init__(self, seller_id: str, serviceable_pincodes: List[str], payment_modes: List[str]):
        self.seller_id = seller_id
        # usage of set for O(1) access time
        self.serviceable_pincodes: Set[str] = set(serviceable_pincodes)
        self.payment_modes: Set[str] = set(payment_modes)
        
        # Inventory Map: ProductId (int) -> Count (int)
        self.inventory: Dict[int, int] = defaultdict(int)

    def add_inventory(self, product_id: int, amount: int):
        self.inventory[product_id] += amount

    def get_inventory(self, product_id: int) -> int:
        return self.inventory[product_id]

    def deduct_inventory(self, product_id: int, amount: int) -> bool:
        """
        Deducts inventory if sufficient stock exists.
        Returns True if successful, False otherwise.
        """
        if self.inventory[product_id] >= amount:
            self.inventory[product_id] -= amount
            return True
        return False

    def supports_pincode(self, pincode: str) -> bool:
        return pincode in self.serviceable_pincodes

    def supports_payment_mode(self, mode: str) -> bool:
        return mode in self.payment_modes