from fastapi import FastAPI, Depends
from sqlmodel import Session
from . import database, schemas
from app.movies_service import (
    list_movies,
    get_movie,
    create_movie,
    update_movie,
    delete_movie,
)

app = FastAPI(title="🎬 Movie Catalogue API")


@app.on_event("startup")
def on_startup():
    database.create_db_and_tables()


@app.get("/movies", response_model=list[schemas.MovieRead])
def list_movies_route(session: Session = Depends(database.get_session)):
    return list_movies(session)


@app.get("/movies/{movie_id}", response_model=schemas.MovieRead)
def get_movie_route(movie_id: int, session: Session = Depends(database.get_session)):
    return get_movie(session, movie_id)


@app.post("/movies", response_model=schemas.MovieRead)
def create_movie_route(
    movie: schemas.MovieCreate, session: Session = Depends(database.get_session)
):
    return create_movie(session, movie)


@app.put("/movies/{movie_id}", response_model=schemas.MovieRead)
def update_movie_route(
    movie_id: int,
    movie_data: schemas.MovieCreate,
    session: Session = Depends(database.get_session),
):
    return update_movie(session, movie_id, movie_data)


@app.delete("/movies/{movie_id}")
def delete_movie_route(movie_id: int, session: Session = Depends(database.get_session)):
    return delete_movie(session, movie_id)
