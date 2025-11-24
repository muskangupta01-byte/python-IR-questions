import uuid
import bisect
from typing import List, Dict, Set, Optional
from models import Room, Booking, BookingStatus

class RoomCatalogService:
    def __init__(self):
        self.rooms_by_id: Dict[str, Room] = {}

    def add_room(self, name: str, capacity: int, features: Set[str]) -> Room:
        room_id = str(uuid.uuid4())
        room = Room(id=room_id, name=name, capacity=capacity, features=features)
        self.rooms_by_id[room_id] = room
        return room

    def get_room(self, room_id: str) -> Optional[Room]:
        return self.rooms_by_id.get(room_id)

    def list_rooms(self) -> List[Room]:
        return list(self.rooms_by_id.values())

    def search_rooms(self, min_capacity: int, required_features: Set[str]) -> List[Room]:
        result = []
        for room in self.rooms_by_id.values():
            if room.capacity >= min_capacity and required_features.issubset(room.features):
                result.append(room)
        return result

class BookingService:
    def __init__(self, room_catalog: RoomCatalogService):
        self.room_catalog = room_catalog
        
        # O(1) Lookup
        self.bookings_by_id: Dict[str, Booking] = {}
        
        # Idempotency: Map request_id -> booking_id
        self.request_dedup: Dict[str, str] = {}
        
        # Schedule: Map room_id -> List[Booking] (Sorted by start_time)
        # This list only contains ACTIVE (CONFIRMED) bookings for conflict checks
        self.room_schedules: Dict[str, List[Booking]] = {}

    def _check_overlap_binary(self, schedule: List[Booking], start: int, end: int) -> bool:
        """
        Uses Binary Search (bisect) to find insertion point and check neighbors.
        Complexity: O(log N)
        """
        if not schedule:
            return False

        # Create a dummy object or use key to find insertion index based on start_time
        # We want to find where 'start' fits in the sorted list of bookings
        keys = [b.start_time for b in schedule]
        idx = bisect.bisect_right(keys, start)

        # Check interaction with the booking BEFORE the insertion point
        # A booking at idx-1 started before our new booking. 
        # If it ends after our new booking starts, it's an overlap.
        if idx > 0:
            prev_booking = schedule[idx - 1]
            # Logic: s1 < e2. Here s1 is new_start, e2 is prev_end.
            if start < prev_booking.end_time:
                return True

        # Check interaction with the booking AFTER the insertion point
        # A booking at idx starts at or after our new booking.
        # If it starts before our new booking ends, it's an overlap.
        if idx < len(schedule):
            next_booking = schedule[idx]
            # Logic: s2 < e1. Here s2 is next_start, e1 is new_end.
            if next_booking.start_time < end:
                return True

        return False

    def book_room(self, user_id: str, room_id: str, start: int, end: int, request_id: str) -> Booking:
        # 1. Validation
        if start >= end:
            raise ValueError("Start time must be before end time")
        
        room = self.room_catalog.get_room(room_id)
        if not room:
            raise ValueError("Room does not exist")

        # 2. Idempotency Check
        if request_id in self.request_dedup:
            existing_booking_id = self.request_dedup[request_id]
            existing_booking = self.bookings_by_id[existing_booking_id]
            
            # Verify params match
            if (existing_booking.room_id != room_id or 
                existing_booking.start_time != start or 
                existing_booking.end_time != end):
                raise ValueError("Idempotency conflict: Request ID exists with different parameters")
            
            return existing_booking

        # 3. Conflict Detection (Binary Search)
        if room_id not in self.room_schedules:
            self.room_schedules[room_id] = []
        
        schedule = self.room_schedules[room_id]
        
        if self._check_overlap_binary(schedule, start, end):
            raise ValueError("Time slot unavailable")

        # 4. Create Booking
        new_booking_id = str(uuid.uuid4())
        booking = Booking(
            id=new_booking_id,
            room_id=room_id,
            user_id=user_id,
            start_time=start,
            end_time=end
        )

        # 5. Commit Data
        self.bookings_by_id[new_booking_id] = booking
        self.request_dedup[request_id] = new_booking_id
        
        # Insert into sorted schedule maintaining order
        # We simply recreate the insert logic to keep it sorted
        keys = [b.start_time for b in schedule]
        idx = bisect.bisect_right(keys, start)
        schedule.insert(idx, booking)

        return booking

    def cancel_booking(self, booking_id: str, user_id: str) -> Booking:
        booking = self.bookings_by_id.get(booking_id)
        if not booking:
            raise ValueError("Booking not found")
        
        if booking.status == BookingStatus.CANCELLED:
            return booking

        # Mark as cancelled
        booking.status = BookingStatus.CANCELLED
        
        # Remove from active schedule to free up the slot for O(log n) checks
        if booking.room_id in self.room_schedules:
            # List remove is O(N), but necessary for the "schedules" list 
            # to remain strictly valid for binary search.
            # In a DB system, this would be an index update.
            try:
                self.room_schedules[booking.room_id].remove(booking)
            except ValueError:
                pass # Already removed
        
        return booking

    def get_room_bookings(self, room_id: str) -> List[Booking]:
        # Return all bookings (including cancelled ones) from the ID map
        # Filtering for the specific room
        return [b for b in self.bookings_by_id.values() if b.room_id == room_id]