from fastapi import APIRouter, Depends, status
from typing import List
from services.admin_room_crud import AdminRoomCrud
from schemas.admin_room_schema import AddRoom, UpdateRoom, RoomOut
from services.admin_auth import get_current_admin

admin_room_router = APIRouter(prefix="/admin/rooms",tags=["Admin Rooms"])


@admin_room_router.post("/", response_model=RoomOut, status_code=status.HTTP_201_CREATED)
async def create_room(
    room_data: AddRoom,
    admin_room_crud: AdminRoomCrud = Depends(),
    token: str = Depends(get_current_admin)
):
    """
    Create a new room (Admin only)
    """
    return admin_room_crud.add_room(room_data)


@admin_room_router.delete("/{room_id}", status_code=status.HTTP_200_OK)
async def delete_room(
    room_id: int,
    admin_room_crud: AdminRoomCrud = Depends(),
    token: str = Depends(get_current_admin)
):
    """
    Delete a room by ID (Admin only)
    """
    return admin_room_crud.delete_room(room_id)


@admin_room_router.put("/{room_id}", response_model=RoomOut)
async def update_room(
    room_id: int,
    room_data: UpdateRoom,
    admin_room_crud: AdminRoomCrud = Depends(),
    token: str = Depends(get_current_admin)
):
    """
    Update a room by ID (Admin only)
    """
    return admin_room_crud.update_room(room_id, room_data)


@admin_room_router.get("/", response_model=List[RoomOut])
async def get_all_rooms(
    admin_room_crud: AdminRoomCrud = Depends(),
    token: str = Depends(get_current_admin)
):
    """
    Get all rooms (Admin only)
    """
    return admin_room_crud.get_all_rooms()


@admin_room_router.get("/{room_id}", response_model=RoomOut)
async def get_room_by_id(
    room_id: int,
    admin_room_crud: AdminRoomCrud = Depends(),
    token: str = Depends(get_current_admin)
):
    """
    Get a room by ID (Admin only)
    """
    return admin_room_crud.get_room_by_id(room_id)