import threading
from typing import Dict
from models import User
from transactions import TransactionFactory
from strategies import UPIStrategy, CreditCardStrategy
from observers import SMSNotification, EmailNotification

class WalletSystem:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(WalletSystem, cls).__new__(cls)
                    cls._instance.users = {}
                    # Idempotency: Map txn_id -> TransactionStatus
                    cls._instance.processed_txns: Dict[str, str] = {}
                    cls._instance.sys_lock = threading.Lock()
        return cls._instance

    def register_user(self, user_id: str, name: str):
        if user_id in self.users:
            raise ValueError("User already exists")
        self.users[user_id] = User(user_id, name)
        print(f"User {name} registered.")

    def get_user(self, user_id):
        return self.users.get(user_id)

    def _check_idempotency(self, txn_id: str):
        with self.sys_lock:
            if txn_id in self.processed_txns:
                return self.processed_txns[txn_id]
            self.processed_txns[txn_id] = "PROCESSING"
            return None

    def add_money(self, txn_id: str, user_id: str, amount: float, source_type: str, details: dict):
        # Idempotency Check
        existing_status = self._check_idempotency(txn_id)
        if existing_status:
            print(f"⚠️ Txn {txn_id} is duplicate. Current Status: {existing_status}")
            return

        user = self.get_user(user_id)
        if not user: raise ValueError("User not found")

        # Strategy Selection
        if source_type == "UPI":
            strategy = UPIStrategy()
        else:
            strategy = CreditCardStrategy()

        # Factory Creation
        txn = TransactionFactory.create_add_money(txn_id, amount, user, strategy, details)
        
        # Attach Observers
        txn.add_observer(SMSNotification())

        # Execute
        txn.execute()

        # Update Idempotency Map
        with self.sys_lock:
            self.processed_txns[txn_id] = txn.status.value

    def transfer_money(self, txn_id: str, from_user: str, to_user: str, amount: float):
        # Idempotency Check
        existing_status = self._check_idempotency(txn_id)
        if existing_status:
            print(f"⚠️ Txn {txn_id} is duplicate. Current Status: {existing_status}")
            return

        sender = self.get_user(from_user)
        receiver = self.get_user(to_user)
        
        # Factory Creation
        txn = TransactionFactory.create_transfer(txn_id, amount, sender, receiver)
        
        # Attach Observers
        txn.add_observer(SMSNotification())
        txn.add_observer(EmailNotification())

        # Execute
        txn.execute()

        # Update Idempotency Map
        with self.sys_lock:
            self.processed_txns[txn_id] = txn.status.value

    def get_statement(self, user_id):
        user = self.get_user(user_id)
        print(f"\n--- Statement for {user.name} ---")
        print(f"Current Balance: {user.wallet.balance}")
        # Sort desc by timestamp
        sorted_txns = sorted(user.wallet.transactions, key=lambda x: x.timestamp, reverse=True)
        for t in sorted_txns:
            print(f"ID: {t.txn_id} | Type: {t.txn_type.value} | Amt: {t.amount} | Status: {t.status.value}")