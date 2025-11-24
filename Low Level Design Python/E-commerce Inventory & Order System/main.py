from inventory_system import InventoryManagementSystem, Helper04

def run_test_cases():
    # 1. Setup
    system = InventoryManagementSystem()
    helper = Helper04()
    
    print("--- Initialization ---")
    system.init(helper, 10)

    print("\n--- Creating Sellers ---")
    # Create Seller 0
    system.createSeller(
        "seller-0", 
        ["110001", "560092", "452001", "700001"], 
        ["netbanking", "cash", "upi"]
    )
    
    # Create Seller 1
    system.createSeller(
        "seller-1", 
        ["400050", "110001", "600032", "560092"], 
        ["netbanking", "cash", "upi"]
    )

    print("\n--- Adding Inventory ---")
    system.addInventory(0, "seller-1", 52)
    print("Added 52 items of Product 0 to Seller 1")
    
    system.addInventory(0, "seller-0", 32)
    print("Added 32 items of Product 0 to Seller 0")

    print("\n--- Processing Orders ---")
    
    # Order 1: Valid order for Seller 1
    # Pincode 400050 is in Seller 1's list
    result_1 = system.createOrder("order-1", "400050", "seller-1", 0, 5, "upi")
    print(f"Order-1 Result: {result_1}") # Expected: order placed

    # Check Inventory for Seller 1 (Should be 52 - 5 = 47)
    inv_1 = system.getInventory(0, "seller-1")
    print(f"Seller-1 Inventory for Product 0: {inv_1}") # Expected: 47

    # Order 2: Valid order for Seller 0
    # Pincode 560092 is in Seller 0's list
    result_2 = system.createOrder("order-2", "560092", "seller-0", 0, 1, "upi")
    print(f"Order-2 Result: {result_2}") # Expected: order placed

    # Check Inventory for Seller 0 (Should be 32 - 1 = 31)
    inv_0 = system.getInventory(0, "seller-0")
    print(f"Seller-0 Inventory for Product 0: {inv_0}") # Expected: 31
    
    print("\n--- Testing Error Conditions ---")
    
    # Test 1: Unserviceable Pincode (999999 is not in Seller 0's list)
    error_1 = system.createOrder("order-3", "999999", "seller-0", 0, 1, "upi")
    print(f"Error Test 1 (Bad Pincode): {error_1}") # Expected: pincode unserviceable
    
    # Test 2: Payment not supported (Seller 0 does not support 'credit card')
    error_2 = system.createOrder("order-4", "110001", "seller-0", 0, 1, "credit card")
    print(f"Error Test 2 (Bad Payment): {error_2}") # Expected: payment mode not supported
    
    # Test 3: Insufficient Inventory (Trying to buy 100 items from Seller 0 who has 31)
    error_3 = system.createOrder("order-5", "110001", "seller-0", 0, 100, "upi")
    print(f"Error Test 3 (Low Inventory): {error_3}") # Expected: insufficient product inventory

if __name__ == "__main__":
    run_test_cases()