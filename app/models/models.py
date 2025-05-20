from sqlalchemy import Column, Integer, String, ForeignKey, text, UniqueConstraint, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("now()"))

    bookings = relationship("Booking", back_populates="user")


class Admin(Base):
    __tablename__ = "admins"

    admin_id = Column(Integer, nullable=False, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("now()"))


class Room(Base):
    __tablename__ = "rooms"

    room_id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, unique=True, nullable=False)  # օրինակ՝ Red, Green
    rows = Column(Integer,)                  # օրինակ՝ 10 տող
    seats_per_row = Column(Integer)          # օրինակ՝ 8 նստատեղ յուրաքանչյուր տողի համար

    shows = relationship("Show", back_populates="room")


class Movie(Base):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    poster_url = Column(String, nullable=True)

    shows = relationship("Show", back_populates="movie")


class Show(Base):
    __tablename__ = "shows"

    show_id = Column(Integer, primary_key=True, nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.movie_id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.room_id"), nullable=False)
    start_time = Column(TIMESTAMP, nullable=False)

    movie = relationship("Movie", back_populates="shows")
    room = relationship("Room", back_populates="shows")
    bookings = relationship("Booking", back_populates="show")


class Booking(Base):
    __tablename__ = "bookings"

    booking_id = Column(Integer, primary_key=True, nullable=False)
    show_id = Column(Integer, ForeignKey("shows.show_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    seat_row = Column(Integer, nullable=False)
    seat_number = Column(Integer, nullable=False)
    booked_at = Column(TIMESTAMP, nullable=False, server_default=text("now()"))
    # QR
    # Senyaki id
    show = relationship("Show", back_populates="bookings")
    user = relationship("User", back_populates="bookings")

    __table_args__ = (
        UniqueConstraint("show_id", "seat_row", "seat_number", name="unique_seat_per_show"),
    )
