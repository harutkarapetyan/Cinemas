# Cinema Booking System – Test Assignment

This is a backend application for a cinema booking system, built as part of a test task for a Back-end Developer position.

## Task Requirements (Brief)

- There are multiple **cinema rooms** (e.g. red, blue, green)
- Each room can show **different movies** at **different times**
- Every movie has a **title** and a **poster**
- Each room has a seating grid (e.g. **10 rows x 8 seats**)
- A **user can book a seat** during a selected movie show
- After booking, the **seat becomes unavailable**
- Admin panel for **managing rooms and movies** (CRUD)

---

## Tech Stack

- **Python** & **FastAPI**
- **SQLAlchemy** (ORM)
- **PostgreSQL** (can be swapped)
- **Pydantic** (data validation)
- **Alembic** (optional for DB migrations)
- JWT-based **Authentication**

---

## How to Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/yourname/cinema-booking-app.git
cd cinema-booking-app

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up database (PostgreSQL or SQLite)
# update database URL in .env or config.py

# 5. Run the application
uvicorn app.main:app --reload
