import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo.db")

BASE_DIR = Path(__file__).resolve().parent.parent
if DATABASE_URL.startswith("sqlite") and not DATABASE_URL.startswith("sqlite:///"):
    DATABASE_URL = f"sqlite:///{BASE_DIR / DATABASE_URL.split('///', 1)[1]}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
