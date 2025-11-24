from typing import List, Set
from models import Room, Booking
from services import RoomCatalogService, BookingService

class MeetingRoomController:
    def __init__(self):
        self.catalog_service = RoomCatalogService()
        self.booking_service = BookingService(self.catalog_service)

    def create_room(self, name: str, capacity: int, features: Set[str]) -> Room:
        return self.catalog_service.add_room(name, capacity, features)

    def list_rooms(self) -> List[Room]:
        return self.catalog_service.list_rooms()

    def search_rooms(self, min_capacity: int, features: Set[str]) -> List[Room]:
        return self.catalog_service.search_rooms(min_capacity, features)

    def book_room(self, user_id: str, room_id: str, start_time: int, end_time: int, request_id: str) -> Booking:
        return self.booking_service.book_room(user_id, room_id, start_time, end_time, request_id)

    def cancel_booking(self, booking_id: str, user_id: str) -> Booking:
        return self.booking_service.cancel_booking(booking_id, user_id)
        
    def get_booking_history(self, room_id: str) -> List[Booking]:
        return self.booking_service.get_room_bookings(room_id)