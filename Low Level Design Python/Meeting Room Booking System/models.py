from dataclasses import dataclass, field
from typing import Set
from enum import Enum

class BookingStatus(Enum):
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"

@dataclass
class Room:
    id: str
    name: str
    capacity: int
    features: Set[str]

@dataclass
class Booking:
    id: str
    room_id: str
    user_id: str
    start_time: int
    end_time: int
    status: BookingStatus = BookingStatus.CONFIRMED