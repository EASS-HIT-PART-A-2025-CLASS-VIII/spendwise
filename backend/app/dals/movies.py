from sqlmodel import Session, select
from app.models.movie import Movie


class MovieDal:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        return self.session.exec(select(Movie)).all()

    def get(self, movie_id: int):
        return self.session.get(Movie, movie_id)

    def create(self, movie: Movie):
        self.session.add(movie)
        self.session.commit()
        self.session.refresh(movie)
        return movie

    def update(self, movie: Movie):
        self.session.add(movie)
        self.session.commit()
        self.session.refresh(movie)
        return movie

    def delete(self, movie: Movie):
        self.session.delete(movie)
        self.session.commit()
