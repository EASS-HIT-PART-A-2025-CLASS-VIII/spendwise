from fastapi import HTTPException
from sqlmodel import Session
from app import models, schemas, crud


def list_movies(session: Session):
    return crud.get_movies(session)


def get_movie(session: Session, movie_id: int):
    movie = crud.get_movie(session, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


def create_movie(session: Session, movie_data: schemas.MovieCreate):
    movie = models.Movie(**movie_data.model_dump())
    return crud.create_movie(session, movie)


def update_movie(session: Session, movie_id: int, movie_data: schemas.MovieCreate):
    updated = crud.update_movie(session, movie_id, movie_data.model_dump())
    if not updated:
        raise HTTPException(status_code=404, detail="Movie not found")
    return updated


def delete_movie(session: Session, movie_id: int):
    deleted = crud.delete_movie(session, movie_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"ok": True}
