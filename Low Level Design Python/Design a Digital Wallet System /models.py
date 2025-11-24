import threading
from enum import Enum
from typing import List, Dict
from dataclasses import dataclass, field
import time

class TransactionStatus(Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

class TransactionType(Enum):
    ADD_MONEY = "ADD_MONEY"
    P2P_TRANSFER = "P2P_TRANSFER"

@dataclass
class TransactionDTO:
    txn_id: str
    amount: float
    timestamp: float
    txn_type: TransactionType
    source_id: str
    target_id: str
    status: TransactionStatus

class Wallet:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.balance = 0.0
        # Reentrant lock for thread safety on individual wallet operations
        self.lock = threading.RLock()
        self.transactions: List[TransactionDTO] = []

    def add_balance(self, amount: float):
        with self.lock:
            self.balance += amount

    def deduct_balance(self, amount: float):
        with self.lock:
            if self.balance < amount:
                raise ValueError("Insufficient Balance")
            self.balance -= amount

    def add_transaction_record(self, record: TransactionDTO):
        with self.lock:
            self.transactions.append(record)

class User:
    def __init__(self, user_id: str, name: str):
        self.user_id = user_id
        self.name = name
        self.wallet = Wallet(user_id)