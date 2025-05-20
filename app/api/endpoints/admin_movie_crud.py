from fastapi import APIRouter, Depends, status
from typing import List
from services.admin_movie_crud import AdminMovieCrud
from schemas.admin_movie_schema import AddMovie, UpdateMovie, MovieOut

from services.admin_auth import get_current_admin

admin_movie_router = APIRouter(prefix="/admin/movies",tags=["Admin Movies"])


@admin_movie_router.post("/", response_model=MovieOut, status_code=status.HTTP_201_CREATED)
async def create_movie(
    movie_data: AddMovie,
    admin_movie_crud: AdminMovieCrud = Depends(),
    token: str = Depends(get_current_admin)
):
    """
    Create a new movie (Admin only)
    """
    return admin_movie_crud.add_movie(movie_data)


@admin_movie_router.delete("/{movie_id}", status_code=status.HTTP_200_OK)
async def delete_movie(
    movie_id: int,
    admin_movie_crud: AdminMovieCrud = Depends(),
    token: str = Depends(get_current_admin)
):
    """
    Delete a movie by ID (Admin only)
    """
    return admin_movie_crud.delete_movie(movie_id)


@admin_movie_router.put("/{movie_id}", response_model=MovieOut)
async def update_movie(
    movie_id: int,
    movie_data: UpdateMovie,
    admin_movie_crud: AdminMovieCrud = Depends(),
    token: str = Depends(get_current_admin)
):
    """
    Update a movie by ID (Admin only)
    """
    return admin_movie_crud.update_movie(movie_id, movie_data)


@admin_movie_router.get("/", response_model=List[MovieOut])
async def get_all_movies(
    admin_movie_crud: AdminMovieCrud = Depends(),
    token: str = Depends(get_current_admin)
):
    """
    Get all movies (Admin only)
    """
    return admin_movie_crud.get_all_movies()


@admin_movie_router.get("/{movie_id}", response_model=MovieOut)
async def get_movie_by_id(
    movie_id: int,
    admin_movie_crud: AdminMovieCrud = Depends(),
    token: str = Depends(get_current_admin)
):
    """
    Get a movie by ID (Admin only)
    """
    return admin_movie_crud.get_movie_by_id(movie_id)
