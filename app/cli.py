import typer
from sqlmodel import Session, select
from .database import engine, create_db_and_tables
from .models import Movie

app = typer.Typer(help="🎬 Manage the Movie Catalogue database")

@app.command()
def seed():
    """Seed the database with a larger set of sample movies (≈50)."""
    create_db_and_tables()
    with Session(engine) as session:
        movies = [
            Movie(title="Inception", director="Christopher Nolan", year=2010, rating=8.8),
            Movie(title="The Matrix", director="Lana Wachowski", year=1999, rating=8.7),
            Movie(title="Parasite", director="Bong Joon-ho", year=2019, rating=8.6),
            Movie(title="Interstellar", director="Christopher Nolan", year=2014, rating=8.6),
            Movie(title="Fight Club", director="David Fincher", year=1999, rating=8.8),
            Movie(title="The Shawshank Redemption", director="Frank Darabont", year=1994, rating=9.3),
            Movie(title="The Dark Knight", director="Christopher Nolan", year=2008, rating=9.0),
            Movie(title="Pulp Fiction", director="Quentin Tarantino", year=1994, rating=8.9),
            Movie(title="Forrest Gump", director="Robert Zemeckis", year=1994, rating=8.8),
            Movie(title="The Godfather", director="Francis Ford Coppola", year=1972, rating=9.2),
            Movie(title="The Godfather Part II", director="Francis Ford Coppola", year=1974, rating=9.0),
            Movie(title="Gladiator", director="Ridley Scott", year=2000, rating=8.5),
            Movie(title="Titanic", director="James Cameron", year=1997, rating=7.8),
            Movie(title="Avatar", director="James Cameron", year=2009, rating=7.9),
            Movie(title="Whiplash", director="Damien Chazelle", year=2014, rating=8.5),
            Movie(title="La La Land", director="Damien Chazelle", year=2016, rating=8.0),
            Movie(title="The Prestige", director="Christopher Nolan", year=2006, rating=8.5),
            Movie(title="Memento", director="Christopher Nolan", year=2000, rating=8.4),
            Movie(title="The Social Network", director="David Fincher", year=2010, rating=7.7),
            Movie(title="The Silence of the Lambs", director="Jonathan Demme", year=1991, rating=8.6),
            Movie(title="Se7en", director="David Fincher", year=1995, rating=8.6),
            Movie(title="Django Unchained", director="Quentin Tarantino", year=2012, rating=8.4),
            Movie(title="Inglourious Basterds", director="Quentin Tarantino", year=2009, rating=8.3),
            Movie(title="The Hateful Eight", director="Quentin Tarantino", year=2015, rating=7.8),
            Movie(title="Once Upon a Time in Hollywood", director="Quentin Tarantino", year=2019, rating=7.6),
            Movie(title="Goodfellas", director="Martin Scorsese", year=1990, rating=8.7),
            Movie(title="The Departed", director="Martin Scorsese", year=2006, rating=8.5),
            Movie(title="Shutter Island", director="Martin Scorsese", year=2010, rating=8.2),
            Movie(title="The Wolf of Wall Street", director="Martin Scorsese", year=2013, rating=8.2),
            Movie(title="Oppenheimer", director="Christopher Nolan", year=2023, rating=8.5),
            Movie(title="The Imitation Game", director="Morten Tyldum", year=2014, rating=8.0),
            Movie(title="The King's Speech", director="Tom Hooper", year=2010, rating=8.0),
            Movie(title="The Pianist", director="Roman Polanski", year=2002, rating=8.5),
            Movie(title="Saving Private Ryan", director="Steven Spielberg", year=1998, rating=8.6),
            Movie(title="Catch Me If You Can", director="Steven Spielberg", year=2002, rating=8.1),
            Movie(title="Schindler's List", director="Steven Spielberg", year=1993, rating=9.0),
            Movie(title="Jaws", director="Steven Spielberg", year=1975, rating=8.0),
            Movie(title="E.T. the Extra-Terrestrial", director="Steven Spielberg", year=1982, rating=7.9),
            Movie(title="The Green Mile", director="Frank Darabont", year=1999, rating=8.6),
            Movie(title="American Beauty", director="Sam Mendes", year=1999, rating=8.3),
            Movie(title="1917", director="Sam Mendes", year=2019, rating=8.3),
            Movie(title="Arrival", director="Denis Villeneuve", year=2016, rating=8.0),
            Movie(title="Blade Runner 2049", director="Denis Villeneuve", year=2017, rating=8.0),
            Movie(title="Prisoners", director="Denis Villeneuve", year=2013, rating=8.1),
            Movie(title="Dune", director="Denis Villeneuve", year=2021, rating=8.2),
            Movie(title="The Grand Budapest Hotel", director="Wes Anderson", year=2014, rating=8.1),
            Movie(title="Isle of Dogs", director="Wes Anderson", year=2018, rating=7.8),
            Movie(title="The French Dispatch", director="Wes Anderson", year=2021, rating=7.2),
            Movie(title="Her", director="Spike Jonze", year=2013, rating=8.0),
            Movie(title="Ex Machina", director="Alex Garland", year=2014, rating=7.7),
        ]
        session.add_all(movies)
        session.commit()
        typer.echo(f"✅ Seeded database with {len(movies)} movies.")

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
    """❗ Delete all movies from the database (keeps the schema)."""
    create_db_and_tables()
    with Session(engine) as session:
        deleted_count = session.query(Movie).delete()
        session.commit()
        typer.echo(f"🧹 Deleted {deleted_count} movie(s) from the database.")


if __name__ == "__main__":
    app()
