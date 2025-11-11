from sqlmodel import Session, select
from .models import Movie


def get_movies(session: Session):
    return session.exec(select(Movie)).all()


def get_movie(session: Session, movie_id: int):
    return session.get(Movie, movie_id)


def create_movie(session: Session, movie: Movie):
    session.add(movie)
    session.commit()
    session.refresh(movie)
    return movie


def update_movie(session: Session, movie_id: int, new_data: dict):
    movie = session.get(Movie, movie_id)
    if not movie:
        return None
    for key, value in new_data.items():
        setattr(movie, key, value)
    session.add(movie)
    session.commit()
    session.refresh(movie)
    return movie


def delete_movie(session: Session, movie_id: int):
    movie = session.get(Movie, movie_id)
    if not movie:
        return None
    session.delete(movie)
    session.commit()
    return True
