from controller import MeetingRoomController
from models import BookingStatus

def run_tests():
    controller = MeetingRoomController()
    
    print("--- 1. Init Rooms ---")
    r1 = controller.create_room("Boardroom", 10, {"Projector", "VC"})
    r2 = controller.create_room("Huddle", 4, {"Whiteboard"})
    print(f"Created Rooms: {r1.name}, {r2.name}")

    print("\n--- 2. Search Rooms ---")
    results = controller.search_rooms(5, {"VC"})
    print(f"Search (Cap >= 5, has VC): Found {[r.name for r in results]}")

    print("\n--- 3. Booking Flow & Overlap Logic ---")
    user = "u123"
    
    # Booking A: 10:00 to 11:00
    b1 = controller.book_room(user, r1.id, 1000, 1100, "req-1")
    print(f"Booking 1 (10-11): {b1.status.value}")

    # Booking B: 11:00 to 12:00 (Back-to-back allowed?)
    try:
        b2 = controller.book_room(user, r1.id, 1100, 1200, "req-2")
        print(f"Booking 2 (11-12) Back-to-back: {b2.status.value}")
    except ValueError as e:
        print(f"Booking 2 Failed: {e}")

    # Booking C: 10:30 to 11:30 (Overlap with B1 and B2?)
    try:
        controller.book_room(user, r1.id, 1030, 1130, "req-3")
    except ValueError as e:
        print(f"Booking 3 (10:30-11:30) Overlap Check: FAILED as expected ({e})")

    print("\n--- 4. Idempotency Check ---")
    # Retry req-1 with exact same params
    b1_retry = controller.book_room(user, r1.id, 1000, 1100, "req-1")
    print(f"Retry req-1 (Same params): returned ID {b1_retry.id} (Matches original? {b1_retry.id == b1.id})")

    # Retry req-1 with DIFFERENT params
    try:
        controller.book_room(user, r1.id, 1400, 1500, "req-1")
    except ValueError as e:
        print(f"Retry req-1 (Diff params): FAILED as expected ({e})")

    print("\n--- 5. Cancellation & Rebooking ---")
    # Cancel Booking 1 (10-11)
    controller.cancel_booking(b1.id, user)
    print("Booking 1 Cancelled.")
    
    # Try to book 10:00-11:00 again (Should work now)
    try:
        b4 = controller.book_room(user, r1.id, 1000, 1100, "req-4")
        print(f"Rebooking 10-11 after cancellation: SUCCESS ({b4.id})")
    except ValueError as e:
        print(f"Rebooking failed: {e}")

if __name__ == "__main__":
    run_tests()