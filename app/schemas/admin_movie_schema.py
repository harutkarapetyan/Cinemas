from pydantic import BaseModel


class AddMovie(BaseModel):
    title: str
    poster_url: str


class UpdateMovie(BaseModel):
    title: str | None = None
    poster_url: str | None = None


class MovieOut(BaseModel):
    movie_id: int
    title: str
    poster_url: str