from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.schemas.movie import MovieCreate, MovieRead, MovieUpdate
from app.services.movies_service import MovieService

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get("/", response_model=list[MovieRead])
def list_movies(session: Session = Depends(get_session)):
    return MovieService(session).list_movies()


@router.get("/{movie_id}", response_model=MovieRead)
def get_movie(movie_id: int, session: Session = Depends(get_session)):
    movie = MovieService(session).get_movie(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@router.post("/", response_model=MovieRead)
def create_movie(movie: MovieCreate, session: Session = Depends(get_session)):
    return MovieService(session).create_movie(movie)


@router.put("/{movie_id}", response_model=MovieRead)
def update_movie(
    movie_id: int, movie: MovieUpdate, session: Session = Depends(get_session)
):
    updated = MovieService(session).update_movie(movie_id, movie)
    if not updated:
        raise HTTPException(status_code=404, detail="Movie not found")
    return updated


@router.delete("/{movie_id}")
def delete_movie(movie_id: int, session: Session = Depends(get_session)):
    deleted = MovieService(session).delete_movie(movie_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"message": "Movie deleted"}
