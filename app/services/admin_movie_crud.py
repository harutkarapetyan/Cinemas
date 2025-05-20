from sqlalchemy.orm.session import Session
# FastAPI
from fastapi.exceptions import HTTPException
from fastapi import status, Depends
from database import get_db
from models import models
from schemas.admin_movie_schema import AddMovie, MovieOut, UpdateMovie
from typing import List


class AdminMovieCrud:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def add_movie(self, movie_data: AddMovie) -> MovieOut:
        try:
            # Create new movie instance
            new_movie = models.Movie(
                title=movie_data.title,
                poster_url=movie_data.poster_url
            )
            
            # Add to database
            self.session.add(new_movie)
            self.session.commit()
            self.session.refresh(new_movie)
            
            # Return the created movie
            return MovieOut(
                movie_id=new_movie.movie_id,
                title=new_movie.title,
                poster_url=new_movie.poster_url
            )
            
        except Exception as e:
            self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to add movie: {str(e)}"
            )

    def delete_movie(self, movie_id: int) -> dict:
        try:
            movie = self.session.query(models.Movie).filter(models.Movie.movie_id == movie_id).first()
            if not movie:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Movie with id {movie_id} not found"
                )
            
            self.session.delete(movie)
            self.session.commit()
            
            return {"message": f"Movie with id {movie_id} successfully deleted"}
            
        except HTTPException:
            raise
        except Exception as e:
            self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete movie: {str(e)}"
            )

    def update_movie(self, movie_id: int, movie_data: UpdateMovie) -> MovieOut:
        try:
            movie = self.session.query(models.Movie).filter(models.Movie.movie_id == movie_id).first()
            if not movie:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Movie with id {movie_id} not found"
                )
            
            # Update only provided fields
            if movie_data.title is not None:
                movie.title = movie_data.title
            if movie_data.poster_url is not None:
                movie.poster_url = movie_data.poster_url
            
            self.session.commit()
            self.session.refresh(movie)
            
            return MovieOut(
                movie_id=movie.movie_id,
                title=movie.title,
                poster_url=movie.poster_url
            )
            
        except HTTPException:
            raise
        except Exception as e:
            self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update movie: {str(e)}"
            )

    def get_all_movies(self) -> List[MovieOut]:
        try:
            movies = self.session.query(models.Movie).all()
            return [
                MovieOut(
                    movie_id=movie.movie_id,
                    title=movie.title,
                    poster_url=movie.poster_url
                )
                for movie in movies
            ]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch movies: {str(e)}"
            )

    def get_movie_by_id(self, movie_id: int) -> MovieOut:
        try:
            movie = self.session.query(models.Movie).filter(models.Movie.movie_id == movie_id).first()
            if not movie:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Movie with id {movie_id} not found"
                )
            
            return MovieOut(
                movie_id=movie.movie_id,
                title=movie.title,
                poster_url=movie.poster_url
            )
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch movie: {str(e)}"
            )
