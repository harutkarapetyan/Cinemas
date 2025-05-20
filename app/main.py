from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import router
from fastapi.responses import FileResponse


app = FastAPI(
    title="Cinema API",
    description="API for Cinema Management System",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Welcome to Cinema API"}


@app.get("/admin-auth-html")
def get_admin_auth_html():
    return FileResponse("../CinemaFront/admin_auth.html", media_type="text/html")


@app.get("/dashboard.html")
def get_dashboard_html():
    return FileResponse("../CinemaFront/dashboard.html", media_type="text/html")