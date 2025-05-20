from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .admin_movie_schema import MovieOut
from .admin_room_schema import RoomOut


class ShowBase(BaseModel):
    movie_id: int
    room_id: int
    start_time: datetime


class ShowCreate(ShowBase):
    pass


class ShowOut(ShowBase):
    show_id: int
    movie: MovieOut
    room: RoomOut

    class Config:
        from_attributes = True


class ShowUpdate(BaseModel):
    movie_id: Optional[int] = None
    room_id: Optional[int] = None
    start_time: Optional[datetime] = None 