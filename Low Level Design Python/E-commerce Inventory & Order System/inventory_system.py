from typing import List, Dict
from models import Seller

class Helper04:
    """Mock helper class for logging"""
    def log(self, message: str):
        print(f"[LOG]: {message}")

class InventoryManagementSystem:
    def __init__(self):
        self.helper = None
        self.products_count = 0
        self.sellers: Dict[str, Seller] = {}

    def init(self, helper: Helper04, products_count: int):
        """
        Initialize global variables and system state.
        """
        self.helper = helper
        self.products_count = products_count
        self.sellers = {}
        if self.helper:
            self.helper.log(f"System initialized with {products_count} products")

    def createSeller(self, seller_id: str, serviceable_pincodes: List[str], payment_modes: List[str]):
        """
        Creates a new seller with defined serviceable area and payment methods.
        """
        if seller_id in self.sellers:
            if self.helper:
                self.helper.log(f"Seller {seller_id} already exists")
            return

        new_seller = Seller(seller_id, serviceable_pincodes, payment_modes)
        self.sellers[seller_id] = new_seller

    def addInventory(self, product_id: int, seller_id: str, delta: int):
        """
        Adds stock for a specific product to a specific seller.
        """
        # Basic validation (though prompt implies valid inputs)
        if product_id < 0 or product_id >= self.products_count:
            return 

        seller = self.sellers.get(seller_id)
        if seller:
            seller.add_inventory(product_id, delta)

    def getInventory(self, product_id: int, seller_id: str) -> int:
        """
        Returns current stock count. Returns 0 if seller/product invalid.
        """
        seller = self.sellers.get(seller_id)
        if not seller:
            return 0
        return seller.get_inventory(product_id)

    def createOrder(self, order_id: str, destination_pincode: str, seller_id: str, 
                    product_id: int, product_count: int, payment_mode: str) -> str:
        """
        Validates and processes an order.
        Order of checks:
        1. Serviceability (Pincode)
        2. Payment Support
        3. Inventory Availability
        """
        seller = self.sellers.get(seller_id)

        # 0. Check if seller exists (Defensive check, though prompt implies valid sellerId)
        if not seller:
            return "seller not found" 

        # 1. Check Pincode Serviceability
        if not seller.supports_pincode(destination_pincode):
            return "pincode unserviceable"

        # 2. Check Payment Mode Support
        if not seller.supports_payment_mode(payment_mode):
            return "payment mode not supported"

        # 3. Check Inventory Availability
        current_stock = seller.get_inventory(product_id)
        if current_stock < product_count:
            return "insufficient product inventory"

        # 4. Process Order
        seller.deduct_inventory(product_id, product_count)
        return "order placed"