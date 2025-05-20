from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import models
from datetime import datetime, timedelta
import random
from passlib.context import CryptContext

# Create tables
models.Base.metadata.create_all(bind=engine)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def seed_database():
    db = SessionLocal()
    try:
        # Clear existing data
        db.query(models.Booking).delete()
        db.query(models.Show).delete()
        db.query(models.Movie).delete()
        db.query(models.Room).delete()
        db.query(models.User).delete()
        db.query(models.Admin).delete()
        db.commit()

        # Create admin users
        admin1 = models.Admin(
            first_name="Admin",
            last_name="User",
            email="admin@cinema.com",
            password=pwd_context.hash("admin123"),
            status=True
        )
        admin2 = models.Admin(
            first_name="Super",
            last_name="Admin",
            email="superadmin@cinema.com",
            password=pwd_context.hash("super123"),
            status=True
        )
        db.add_all([admin1, admin2])

        # Create regular users
        users = []
        for i in range(5):
            user = models.User(
                first_name=f"User{i+1}",
                last_name=f"Test{i+1}",
                email=f"user{i+1}@test.com",
                password=pwd_context.hash(f"user{i+1}pass"),
                status=True
            )
            users.append(user)
        db.add_all(users)

        # Create rooms
        rooms = []
        room_names = ["Red", "Blue", "Green", "Yellow", "Purple"]
        for i in range(5):
            room = models.Room(
                name=room_names[i],
                rows=random.randint(8, 12),
                seats_per_row=random.randint(10, 15)
            )
            rooms.append(room)
        db.add_all(rooms)

        # Create movies
        movies = []
        movie_titles = [
            "The Matrix",
            "Inception",
            "Interstellar",
            "The Dark Knight",
            "Pulp Fiction",
            "Forrest Gump",
            "The Godfather",
            "Titanic"
        ]
        for title in movie_titles:
            movie = models.Movie(
                title=title,
                poster_url=f"https://example.com/posters/{title.lower().replace(' ', '_')}.jpg"
            )
            movies.append(movie)
        db.add_all(movies)

        # Commit to get IDs
        db.commit()

        # Create shows
        shows = []
        start_date = datetime.now()
        for movie in movies:
            for room in rooms:
                # Create 3 shows for each movie in each room
                for i in range(3):
                    show_time = start_date + timedelta(days=i, hours=random.randint(10, 20))
                    show = models.Show(
                        movie_id=movie.movie_id,
                        room_id=room.room_id,
                        start_time=show_time
                    )
                    shows.append(show)
        db.add_all(shows)

        # Commit to get show IDs
        db.commit()

        # Create bookings
        bookings = []
        for show in shows:
            # Create 5-10 random bookings for each show
            num_bookings = random.randint(5, 10)
            for _ in range(num_bookings):
                booking = models.Booking(
                    show_id=show.show_id,
                    user_id=random.choice(users).user_id,
                    seat_row=random.randint(1, show.room.rows),
                    seat_number=random.randint(1, show.room.seats_per_row),
                    booked_at=datetime.now() - timedelta(days=random.randint(1, 7))
                )
                bookings.append(booking)
        db.add_all(bookings)

        # Final commit
        db.commit()
        print("Database seeded successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database() 