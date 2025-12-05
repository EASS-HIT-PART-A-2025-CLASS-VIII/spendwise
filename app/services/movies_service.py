from sqlmodel import Session
from app.dals.movies import MovieDal
from app.schemas.movie import MovieCreate, MovieUpdate
from app.models.movie import Movie


class MovieService:
    def __init__(self, session: Session):
        self.crud = MovieDal(session)

    def list_movies(self):
        return self.crud.get_all()

    def get_movie(self, movie_id: int):
        return self.crud.get(movie_id)

    def create_movie(self, movie_data: MovieCreate):
        movie = Movie(**movie_data.model_dump())
        return self.crud.create(movie)

    def update_movie(self, movie_id: int, movie_data: MovieUpdate):
        movie = self.crud.get(movie_id)
        if not movie:
            return None

        for field, value in movie_data.model_dump(exclude_unset=True).items():
            setattr(movie, field, value)

        return self.crud.update(movie)

    def delete_movie(self, movie_id: int):
        movie = self.crud.get(movie_id)
        if not movie:
            return None

        self.crud.delete(movie)
        return True
