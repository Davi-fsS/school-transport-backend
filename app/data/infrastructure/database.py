from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
DB_URL = DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL, echo=True, pool_size=20, max_overflow=40, pool_recycle=600, isolation_level="READ UNCOMMITTED")
SessionLocal = sessionmaker(expire_on_commit=True, autoflush=True, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()