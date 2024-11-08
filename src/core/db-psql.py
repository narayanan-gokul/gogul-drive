from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

engine = create_engine(
    "postgresql+psycopg://postgres:jadoogar@localhost:5432",
    connect_args={"password": "goguldrivepgroot"},
)

with Session(engine) as session:
    session.execute(text("CREATE TABLE some_table (x int, y int)"))
    session.commit()
