from abc import ABC, abstractmethod
import time
from models import TransactionStatus, TransactionType, TransactionDTO, User
from strategies import PaymentSourceStrategy
from observers import NotificationObserver
from typing import List

# --- Template Method Pattern ---
class BaseTransaction(ABC):
    def __init__(self, txn_id: str, amount: float):
        self.txn_id = txn_id
        self.amount = amount
        self.status = TransactionStatus.PENDING
        self.timestamp = time.time()
        self.observers: List[NotificationObserver] = []

    def add_observer(self, observer: NotificationObserver):
        self.observers.append(observer)

    def execute(self):
        """
        The Template Method defining the skeleton of a transaction.
        """
        try:
            self.validate()
            self.process()
            self.status = TransactionStatus.SUCCESS
        except Exception as e:
            print(f"❌ Txn {self.txn_id} Failed: {str(e)}")
            self.status = TransactionStatus.FAILED
            self.rollback() # Optional hook
        finally:
            self.notify_observers()
            self.save_history()

    def notify_observers(self):
        record = self.get_record()
        for obs in self.observers:
            obs.update(record)

    @abstractmethod
    def validate(self): pass

    @abstractmethod
    def process(self): pass

    def rollback(self): pass # Default hook

    @abstractmethod
    def save_history(self): pass

    @abstractmethod
    def get_record(self) -> TransactionDTO: pass


class AddMoneyTransaction(BaseTransaction):
    def __init__(self, txn_id: str, amount: float, user: User, 
                 strategy: PaymentSourceStrategy, payment_details: dict):
        super().__init__(txn_id, amount)
        self.user = user
        self.strategy = strategy
        self.payment_details = payment_details

    def validate(self):
        if self.amount <= 0:
            raise ValueError("Amount must be positive")

    def process(self):
        # 1. Charge external source
        success = self.strategy.charge(self.payment_details, self.amount)
        if not success:
            raise Exception("Bank payment failed")
        
        # 2. Update wallet (Thread Safe via Wallet lock)
        self.user.wallet.add_balance(self.amount)

    def save_history(self):
        record = self.get_record()
        self.user.wallet.add_transaction_record(record)

    def get_record(self) -> TransactionDTO:
        return TransactionDTO(
            self.txn_id, self.amount, self.timestamp, 
            TransactionType.ADD_MONEY, "BANK", self.user.user_id, self.status
        )


class P2PTransferTransaction(BaseTransaction):
    def __init__(self, txn_id: str, amount: float, sender: User, receiver: User):
        super().__init__(txn_id, amount)
        self.sender = sender
        self.receiver = receiver

    def validate(self):
        if self.amount <= 0:
            raise ValueError("Amount must be positive")
        if self.sender.user_id == self.receiver.user_id:
            raise ValueError("Cannot send money to self")

    def process(self):
        """
        Handles Concurrency and Deadlocks.
        Acquires locks in a consistent order (based on user_id) to prevent deadlocks.
        """
        # Deadlock Prevention: Sort locks
        first_lock_wallet = self.sender.wallet if self.sender.user_id < self.receiver.user_id else self.receiver.wallet
        second_lock_wallet = self.receiver.wallet if self.sender.user_id < self.receiver.user_id else self.sender.wallet

        # Atomic Transfer
        with first_lock_wallet.lock:
            with second_lock_wallet.lock:
                # Double check balance inside lock
                if self.sender.wallet.balance < self.amount:
                    raise ValueError("Insufficient Balance inside lock")
                
                self.sender.wallet.deduct_balance(self.amount)
                self.receiver.wallet.add_balance(self.amount)

    def save_history(self):
        record = self.get_record()
        # Add to both logs
        self.sender.wallet.add_transaction_record(record)
        self.receiver.wallet.add_transaction_record(record)

    def get_record(self) -> TransactionDTO:
        return TransactionDTO(
            self.txn_id, self.amount, self.timestamp, 
            TransactionType.P2P_TRANSFER, self.sender.user_id, self.receiver.user_id, self.status
        )

# --- Factory Pattern ---
class TransactionFactory:
    @staticmethod
    def create_add_money(txn_id, amount, user, strategy, details):
        return AddMoneyTransaction(txn_id, amount, user, strategy, details)

    @staticmethod
    def create_transfer(txn_id, amount, sender, receiver):
        return P2PTransferTransaction(txn_id, amount, sender, receiver)