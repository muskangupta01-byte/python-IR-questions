from abc import ABC, abstractmethod
from models import TransactionDTO

class NotificationObserver(ABC):
    @abstractmethod
    def update(self, txn_record: TransactionDTO):
        pass

class SMSNotification(NotificationObserver):
    def update(self, txn_record: TransactionDTO):
        print(f"📱 [SMS] Alert: Txn {txn_record.txn_id} status is {txn_record.status.value}")

class EmailNotification(NotificationObserver):
    def update(self, txn_record: TransactionDTO):
        # Only send email on failure for this example
        if txn_record.status == "FAILED":
            print(f"📧 [Email] Alert: Txn {txn_record.txn_id} FAILED.")