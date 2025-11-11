from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
from . import database, models, crud, schemas

app = FastAPI(title="🎬 Movie Catalogue API")


@app.on_event("startup")
def on_startup():
    database.create_db_and_tables()


@app.get("/movies", response_model=list[schemas.MovieRead])
def list_movies(session: Session = Depends(database.get_session)):
    return crud.get_movies(session)


@app.get("/movies/{movie_id}", response_model=schemas.MovieRead)
def get_movie(movie_id: int, session: Session = Depends(database.get_session)):
    movie = crud.get_movie(session, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@app.post("/movies", response_model=schemas.MovieRead)
def create_movie(movie: schemas.MovieCreate, session: Session = Depends(database.get_session)):
    new_movie = models.Movie(**movie.dict())
    return crud.create_movie(session, new_movie)


@app.put("/movies/{movie_id}", response_model=schemas.MovieRead)
def update_movie(movie_id: int, movie_data: schemas.MovieCreate, session: Session = Depends(database.get_session)):
    updated = crud.update_movie(session, movie_id, movie_data.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Movie not found")
    return updated


@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int, session: Session = Depends(database.get_session)):
    deleted = crud.delete_movie(session, movie_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"ok": True}
