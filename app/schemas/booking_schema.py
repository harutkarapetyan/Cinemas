from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BookingBase(BaseModel):
    show_id: int
    seat_row: int
    seat_number: int


class BookingCreate(BookingBase):
    pass


class BookingOut(BookingBase):
    booking_id: int
    user_id: int
    booked_at: datetime

    class Config:
        from_attributes = True


class BookingUpdate(BaseModel):
    show_id: Optional[int] = None
    seat_row: Optional[int] = None
    seat_number: Optional[int] = None 