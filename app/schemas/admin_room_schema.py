from pydantic import BaseModel

class AddRoom(BaseModel):
    name: str
    rows: int
    seats_per_row: int

class UpdateRoom(BaseModel):
    name: str | None = None
    rows: int | None = None
    seats_per_row: int | None = None

class RoomOut(BaseModel):
    room_id: int
    name: str
    rows: int
    seats_per_row: int