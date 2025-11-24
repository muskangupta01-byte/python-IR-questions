from abc import ABC, abstractmethod
from collections import Dict

class PaymentSourceStrategy(ABC):
    """
    Strategy Interface for funding sources.
    """
    @abstractmethod
    def charge(self, details: Dict, amount: float) -> bool:
        pass

class UPIStrategy(PaymentSourceStrategy):
    def charge(self, details: Dict, amount: float) -> bool:
        upi_id = details.get("upi_id")
        print(f"[Mock Bank] Charging {amount} via UPI ID: {upi_id}...")
        return True

class CreditCardStrategy(PaymentSourceStrategy):
    def charge(self, details: Dict, amount: float) -> bool:
        card_num = details.get("card_number")
        print(f"[Mock Bank] Charging {amount} via Card: {card_num}...")
        return True