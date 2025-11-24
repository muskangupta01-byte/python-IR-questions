import threading
import time
from wallet_system import WalletSystem

def run_tests():
    ws = WalletSystem()
    
    # 1. Setup Users
    ws.register_user("u1", "Alice")
    ws.register_user("u2", "Bob")

    # 2. Add Money
    ws.add_money("txn-1", "u1", 1000.0, "UPI", {"upi_id": "alice@upi"})
    ws.add_money("txn-2", "u2", 1000.0, "CARD", {"card_number": "4242"})

    print("\n--- Starting Concurrent P2P Transfers ---")
    
    # 3. Simulate High Concurrency & Potential Deadlock
    # Alice sends to Bob, AND Bob sends to Alice simultaneously
    
    def txn_a_to_b():
        for i in range(5):
            ws.transfer_money(f"t-ab-{i}", "u1", "u2", 10.0)
            time.sleep(0.01)

    def txn_b_to_a():
        for i in range(5):
            ws.transfer_money(f"t-ba-{i}", "u2", "u1", 20.0)
            time.sleep(0.01)

    t1 = threading.Thread(target=txn_a_to_b)
    t2 = threading.Thread(target=txn_b_to_a)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    # 4. Idempotency Test
    print("\n--- Testing Idempotency ---")
    ws.add_money("txn-1", "u1", 500.0, "UPI", {}) # Should be ignored

    # 5. Final Statements
    ws.get_statement("u1")
    ws.get_statement("u2")

if __name__ == "__main__":
    run_tests()