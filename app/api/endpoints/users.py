from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from services.users import UserService, BookingCreate
from models import models
from schemas.admin_room_schema import RoomOut
from schemas.admin_movie_schema import MovieOut
from schemas.booking_schema import BookingOut
from schemas.show_schema import ShowOut
from services.users import ShowBookingStatus, RoomShowsBookingStatus
from services.user_auth import get_current_user

users_router = APIRouter(tags=["Users Router"], prefix="/api/users")


@users_router.get("/all-rooms", response_model=List[RoomOut])
def get_all_rooms(user_service: UserService = Depends(),
                  token: str = Depends(get_current_user)):
    """
    Get all rooms (available to all users)
    """
    return user_service.get_all_rooms() 


@users_router.get("/rooms/{room_id}/movies", response_model=List[MovieOut])
def get_movies_by_room(room_id: int, 
                      user_service: UserService = Depends(),
                      token: str = Depends(get_current_user)):
    """
    Get all movies showing in a specific room
    """
    return user_service.get_all_movies_by_room(room_id)


@users_router.get("/rooms/{room_id}/movies/{movie_id}/bookings", response_model=List[BookingOut])
def get_bookings_by_room_and_movie(
    room_id: int,
    movie_id: int,
    user_service: UserService = Depends(),
    token: str = Depends(get_current_user)
):
    """
    Get all bookings for a specific movie in a specific room
    """
    return user_service.get_all_bookings_by_room_and_movie(room_id, movie_id)


@users_router.get("/shows", response_model=List[ShowOut])
def get_all_shows(user_service: UserService = Depends(),
                 token: str = Depends(get_current_user)):
    """
    Get all shows with their associated movie and room information
    """
    return user_service.get_all_shows()


@users_router.get("/rooms/{room_id}/shows", response_model=List[ShowOut])
def get_shows_by_room(room_id: int, 
                     user_service: UserService = Depends(),
                     token: str = Depends(get_current_user)):
    """
    Get all shows for a specific room with their associated movie information
    """
    return user_service.get_shows_by_room(room_id)


@users_router.get("/shows/{show_id}/booking-status", response_model=ShowBookingStatus)
def get_show_booking_status(show_id: int, 
                          user_service: UserService = Depends(),
                        #   token: str = Depends(get_current_user)):
):
    """
    Get detailed booking status for a specific show, including:
    - Show information (movie, room, time)
    - Total seats
    - Number of booked and available seats
    - Status of each seat (booked/available)
    """
    return user_service.get_show_booking_status(show_id)


@users_router.get("/rooms/{room_id}/booking-status", response_model=RoomShowsBookingStatus)
def get_room_shows_booking_status(room_id: int, 
                                user_service: UserService = Depends(),
                                token: str = Depends(get_current_user)):

    """
    Get detailed booking status for all shows in a specific room, including:
    - Room information
    - For each show:
      - Show information (movie, time)
      - Total seats
      - Number of booked and available seats
      - Status of each seat (booked/available)
    """
    return user_service.get_room_shows_booking_status(room_id)


@users_router.post("/shows/{show_id}/book", response_model=BookingOut)
def book_seat(
    show_id: int,
    booking_data: BookingCreate,
    user_service: UserService = Depends(),
    # token: str = Depends(get_current_user)
):
    """
    Book a seat for a show.
    
    Args:
        show_id: ID of the show to book
        booking_data: Seat booking information (seat_row and seat_number)
        
    Returns:
        The created booking information
        
    Raises:
        404: If show not found
        400: If seat is invalid or already booked
        500: If there's a server error
    """
    # Ensure the show_id in the path matches the one in the booking data
    if show_id != booking_data.show_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Show ID in path does not match show ID in booking data"
        )
    
    return user_service.book_seat(7, booking_data)


