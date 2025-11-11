from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///./movies.db"
engine = create_engine(DATABASE_URL, echo=True)

#Create tables in db if they don't exist
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

#Return db session
def get_session():
    with Session(engine) as session:
        yield session
