import csv
import typer
from sqlmodel import Session, select
from app.database import engine, create_db_and_tables
from app.models.movie import Movie

app = typer.Typer(help="Manage the Movie Catalogue database")


@app.command()
def seed(csv_path: str = "data/movies.csv"):
    """Seed the database with movies from a CSV file."""
    create_db_and_tables()

    with Session(engine) as session:
        try:
            with open(csv_path, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                movies = [
                    Movie(
                        title=row["title"],
                        director=row["director"],
                        year=int(row["year"]),
                        rating=float(row["rating"]) if row.get("rating") else None,
                    )
                    for row in reader
                ]
        except FileNotFoundError:
            typer.echo(f"CSV file not found: {csv_path}")
            raise typer.Exit(code=1)

        session.add_all(movies)
        session.commit()
        typer.echo(f"Seeded database with {len(movies)} movies from {csv_path}")


@app.command()
def list():
    """List all movies currently in the database."""
    with Session(engine) as session:
        result = session.exec(select(Movie)).all()
        if not result:
            typer.echo("No movies found.")
            raise typer.Exit()
        for movie in result:
            typer.echo(f"{movie.id}: {movie.title} ({movie.year}) ⭐ {movie.rating}")


@app.command()
def reset():
    """Delete all movies from the database (keeps the schema)."""
    create_db_and_tables()
    with Session(engine) as session:
        deleted_count = session.query(Movie).delete()
        session.commit()
        typer.echo(f"🧹 Deleted {deleted_count} movie(s) from the database.")


if __name__ == "__main__":
    app()
