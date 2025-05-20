from sqlalchemy.orm.session import Session
# FastAPI
from fastapi.exceptions import HTTPException
from fastapi import status, Depends
from database import get_db
from models import models
# from schemas.
from typing import List, Dict
from schemas.show_schema import ShowOut
from schemas.admin_movie_schema import MovieOut
from schemas.admin_room_schema import RoomOut
from pydantic import BaseModel
from datetime import datetime


class SeatStatus(BaseModel):
    row: int
    number: int
    is_booked: bool
    booking_id: int | None = None


class ShowBookingStatus(BaseModel):
    show_id: int
    movie: MovieOut
    room: RoomOut
    start_time: datetime
    total_seats: int
    booked_seats: int
    available_seats: int
    seats: List[SeatStatus]


class RoomShowsBookingStatus(BaseModel):
    room: RoomOut
    shows: List[ShowBookingStatus]


class BookingCreate(BaseModel):
    show_id: int
    seat_row: int
    seat_number: int


class UserService:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session
    
    def get_all_rooms(self):
        all_rooms = self.session.query(models.Room).all()

        return all_rooms
    
    def get_all_movies_by_room(self, room_id: int) -> List[models.Movie]:
        try:
            # Get all shows for the specified room
            shows = self.session.query(models.Show).filter(models.Show.room_id == room_id).all()
            
            # Extract unique movies from the shows
            movies = []
            seen_movie_ids = set()
            
            for show in shows:
                if show.movie.movie_id not in seen_movie_ids:
                    movies.append(show.movie)
                    seen_movie_ids.add(show.movie.movie_id)
            
            return movies
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch movies for room: {str(e)}"
            )

    def get_all_bookings_by_room_and_movie(self, room_id: int, movie_id: int) -> List[models.Booking]:
        try:
            # First verify that the room and movie exist
            room = self.session.query(models.Room).filter(models.Room.room_id == room_id).first()
            if not room:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Room with id {room_id} not found"
                )

            movie = self.session.query(models.Movie).filter(models.Movie.movie_id == movie_id).first()
            if not movie:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Movie with id {movie_id} not found"
                )

            # Get all shows for the specified room and movie
            shows = self.session.query(models.Show).filter(
                models.Show.room_id == room_id,
                models.Show.movie_id == movie_id
            ).all()

            if not shows:
                return []  # Return empty list if no shows found

            # Get all bookings for these shows
            show_ids = [show.show_id for show in shows]
            bookings = self.session.query(models.Booking).filter(
                models.Booking.show_id.in_(show_ids)
            ).all()

            return bookings

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch bookings: {str(e)}"
            )
    
    def get_all_shows(self) -> List[ShowOut]:
        try:
            # Get all shows with their associated movie and room information
            shows = self.session.query(models.Show).all()
            
            # Convert to ShowOut objects
            return [
                ShowOut(
                    show_id=show.show_id,
                    movie_id=show.movie_id,
                    room_id=show.room_id,
                    start_time=show.start_time,
                    movie=MovieOut(
                        movie_id=show.movie.movie_id,
                        title=show.movie.title,
                        poster_url=show.movie.poster_url
                    ),
                    room=RoomOut(
                        room_id=show.room.room_id,
                        name=show.room.name,
                        rows=show.room.rows,
                        seats_per_row=show.room.seats_per_row
                    )
                )
                for show in shows
            ]
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch shows: {str(e)}"
            )
    
    def get_shows_by_room(self, room_id: int) -> List[ShowOut]:
        try:
            # First verify that the room exists
            room = self.session.query(models.Room).filter(models.Room.room_id == room_id).first()
            if not room:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Room with id {room_id} not found"
                )

            # Get all shows for the specified room
            shows = self.session.query(models.Show).filter(
                models.Show.room_id == room_id
            ).all()
            
            # Convert to ShowOut objects
            return [
                ShowOut(
                    show_id=show.show_id,
                    movie_id=show.movie_id,
                    room_id=show.room_id,
                    start_time=show.start_time,
                    movie=MovieOut(
                        movie_id=show.movie.movie_id,
                        title=show.movie.title,
                        poster_url=show.movie.poster_url
                    ),
                    room=RoomOut(
                        room_id=show.room.room_id,
                        name=show.room.name,
                        rows=show.room.rows,
                        seats_per_row=show.room.seats_per_row
                    )
                )
                for show in shows
            ]
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch shows for room: {str(e)}"
            )
    
    def book_movie():  # move, room, seat...
        pass

    def get_show_booking_status(self, show_id: int) -> ShowBookingStatus:
        try:
            # Get the show with its movie and room information
            show = self.session.query(models.Show).filter(
                models.Show.show_id == show_id
            ).first()
            
            if not show:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Show with id {show_id} not found"
                )

            # Get all bookings for this show
            bookings = self.session.query(models.Booking).filter(
                models.Booking.show_id == show_id
            ).all()

            # Create a set of booked seats for quick lookup
            booked_seats = {
                (booking.seat_row, booking.seat_number): booking.booking_id
                for booking in bookings
            }

            # Calculate total seats
            total_seats = show.room.rows * show.room.seats_per_row
            booked_seats_count = len(bookings)
            available_seats = total_seats - booked_seats_count

            # Create list of all seats with their status
            seats = []
            for row in range(1, show.room.rows + 1):
                for seat_number in range(1, show.room.seats_per_row + 1):
                    is_booked = (row, seat_number) in booked_seats
                    seats.append(
                        SeatStatus(
                            row=row,
                            number=seat_number,
                            is_booked=is_booked,
                            booking_id=booked_seats.get((row, seat_number))
                        )
                    )

            return ShowBookingStatus(
                show_id=show.show_id,
                movie=MovieOut(
                    movie_id=show.movie.movie_id,
                    title=show.movie.title,
                    poster_url=show.movie.poster_url
                ),
                room=RoomOut(
                    room_id=show.room.room_id,
                    name=show.room.name,
                    rows=show.room.rows,
                    seats_per_row=show.room.seats_per_row
                ),
                start_time=show.start_time,
                total_seats=total_seats,
                booked_seats=booked_seats_count,
                available_seats=available_seats,
                seats=seats
            )

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch show booking status: {str(e)}"
            )

    def get_room_shows_booking_status(self, room_id: int) -> RoomShowsBookingStatus:
        try:
            # First verify that the room exists
            room = self.session.query(models.Room).filter(models.Room.room_id == room_id).first()
            if not room:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Room with id {room_id} not found"
                )

            # Get all shows for this room
            shows = self.session.query(models.Show).filter(
                models.Show.room_id == room_id
            ).all()

            if not shows:
                return RoomShowsBookingStatus(
                    room=RoomOut(
                        room_id=room.room_id,
                        name=room.name,
                        rows=room.rows,
                        seats_per_row=room.seats_per_row
                    ),
                    shows=[]
                )

            # Get all bookings for these shows
            show_ids = [show.show_id for show in shows]
            bookings = self.session.query(models.Booking).filter(
                models.Booking.show_id.in_(show_ids)
            ).all()

            # Create a dictionary of bookings by show_id
            bookings_by_show = {}
            for booking in bookings:
                if booking.show_id not in bookings_by_show:
                    bookings_by_show[booking.show_id] = []
                bookings_by_show[booking.show_id].append(booking)

            # Create booking status for each show
            shows_status = []
            for show in shows:
                show_bookings = bookings_by_show.get(show.show_id, [])
                
                # Create a set of booked seats for quick lookup
                booked_seats = {
                    (booking.seat_row, booking.seat_number): booking.booking_id
                    for booking in show_bookings
                }

                # Calculate total seats
                total_seats = room.rows * room.seats_per_row
                booked_seats_count = len(show_bookings)
                available_seats = total_seats - booked_seats_count

                # Create list of all seats with their status
                seats = []
                for row in range(1, room.rows + 1):
                    for seat_number in range(1, room.seats_per_row + 1):
                        is_booked = (row, seat_number) in booked_seats
                        seats.append(
                            SeatStatus(
                                row=row,
                                number=seat_number,
                                is_booked=is_booked,
                                booking_id=booked_seats.get((row, seat_number))
                            )
                        )

                shows_status.append(
                    ShowBookingStatus(
                        show_id=show.show_id,
                        movie=MovieOut(
                            movie_id=show.movie.movie_id,
                            title=show.movie.title,
                            poster_url=show.movie.poster_url
                        ),
                        room=RoomOut(
                            room_id=room.room_id,
                            name=room.name,
                            rows=room.rows,
                            seats_per_row=room.seats_per_row
                        ),
                        start_time=show.start_time,
                        total_seats=total_seats,
                        booked_seats=booked_seats_count,
                        available_seats=available_seats,
                        seats=seats
                    )
                )

            return RoomShowsBookingStatus(
                room=RoomOut(
                    room_id=room.room_id,
                    name=room.name,
                    rows=room.rows,
                    seats_per_row=room.seats_per_row
                ),
                shows=shows_status
            )

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch room shows booking status: {str(e)}"
            )

    def book_seat(self, user_id: int, booking_data: BookingCreate) -> models.Booking:
        """
        Book a seat for a show.
        
        Args:
            user_id: The ID of the user making the booking
            booking_data: BookingCreate object containing show_id, seat_row, and seat_number
            
        Returns:
            The created Booking object
            
        Raises:
            HTTPException: If show not found, seat is invalid, or seat is already booked
        """
        try:
            # Get the show and verify it exists
            show = self.session.query(models.Show).filter(
                models.Show.show_id == booking_data.show_id
            ).first()
            
            if not show:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Show with id {booking_data.show_id} not found"
                )

            # Verify the seat coordinates are valid for the room
            if (booking_data.seat_row < 1 or 
                booking_data.seat_row > show.room.rows or 
                booking_data.seat_number < 1 or 
                booking_data.seat_number > show.room.seats_per_row):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid seat coordinates. Room has {show.room.rows} rows and {show.room.seats_per_row} seats per row"
                )

            # Check if the seat is already booked
            existing_booking = self.session.query(models.Booking).filter(
                models.Booking.show_id == booking_data.show_id,
                models.Booking.seat_row == booking_data.seat_row,
                models.Booking.seat_number == booking_data.seat_number
            ).first()

            if existing_booking:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This seat is already booked"
                )

            # Create the booking
            new_booking = models.Booking(
                show_id=booking_data.show_id,
                user_id=user_id,
                seat_row=booking_data.seat_row,
                seat_number=booking_data.seat_number,
                booked_at=datetime.utcnow()
            )

            # Add and commit the booking
            self.session.add(new_booking)
            self.session.commit()
            self.session.refresh(new_booking)

            return new_booking

        except HTTPException:
            raise
        except Exception as e:
            self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create booking: {str(e)}"
            )
