from sqlalchemy.orm.session import Session
# FastAPI
from fastapi.exceptions import HTTPException
from fastapi import status, Depends
from database import get_db
from models import models
from schemas.admin_room_schema import AddRoom, RoomOut, UpdateRoom
from typing import List


class AdminRoomCrud:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def add_room(self, room_data: AddRoom) -> RoomOut:
        try:
            # Create new room instance
            new_room = models.Room(
                name=room_data.name,
                rows=room_data.rows,
                seats_per_row=room_data.seats_per_row
            )
            
            # Add to database
            self.session.add(new_room)
            self.session.commit()
            self.session.refresh(new_room)
            
            # Return the created room
            return RoomOut(
                room_id=new_room.room_id,
                name=new_room.name,
                rows=new_room.rows,
                seats_per_row=new_room.seats_per_row
            )
            
        except Exception as e:
            self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to add room: {str(e)}"
            )

    def delete_room(self, room_id: int) -> dict:
        try:
            room = self.session.query(models.Room).filter(models.Room.room_id == room_id).first()
            if not room:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Room with id {room_id} not found"
                )
            
            self.session.delete(room)
            self.session.commit()
            
            return {"message": f"Room with id {room_id} successfully deleted"}
            
        except HTTPException:
            raise
        except Exception as e:
            self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete room: {str(e)}"
            )

    def update_room(self, room_id: int, room_data: UpdateRoom) -> RoomOut:
        try:
            room = self.session.query(models.Room).filter(models.Room.room_id == room_id).first()
            if not room:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Room with id {room_id} not found"
                )
            
            # Update only provided fields
            if room_data.name is not None:
                room.name = room_data.name
            if room_data.rows is not None:
                room.rows = room_data.rows
            if room_data.seats_per_row is not None:
                room.seats_per_row = room_data.seats_per_row
            
            self.session.commit()
            self.session.refresh(room)
            
            return RoomOut(
                room_id=room.room_id,
                name=room.name,
                rows=room.rows,
                seats_per_row=room.seats_per_row
            )
            
        except HTTPException:
            raise
        except Exception as e:
            self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update room: {str(e)}"
            )

    def get_all_rooms(self) -> List[RoomOut]:
        try:
            rooms = self.session.query(models.Room).all()
            return [
                RoomOut(
                    room_id=room.room_id,
                    name=room.name,
                    rows=room.rows,
                    seats_per_row=room.seats_per_row
                )
                for room in rooms
            ]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch rooms: {str(e)}"
            )

    def get_room_by_id(self, room_id: int) -> RoomOut:
        try:
            room = self.session.query(models.Room).filter(models.Room.room_id == room_id).first()
            if not room:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Room with id {room_id} not found"
                )
            
            return RoomOut(
                room_id=room.room_id,
                name=room.name,
                rows=room.rows,
                seats_per_row=room.seats_per_row
            )
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch room: {str(e)}"
            )
