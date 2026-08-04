from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

class Base(DeclarativeBase):
    pass

engine = create_engine(
    DATABASE_URL,
    echo=True      # näyttää SQL-lauseet terminaalissa
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

with engine.connect() as conn:
    print("Yhteys ok")
