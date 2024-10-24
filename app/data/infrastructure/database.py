from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
import os

load_dotenv()
DB_URL = DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL, echo=True, pool_size=80, max_overflow=80, pool_recycle=600, isolation_level="READ UNCOMMITTED")
SessionLocal = sessionmaker(expire_on_commit=True, autoflush=True, bind=engine)

Base = declarative_base()

class SessionManager():
    def __init__(self):
        self.session: Session = SessionLocal()

    def get_db(self):
        try:
            yield self.session
        finally:
            self.session.close()

    def close(self, session: Session):
        session.close()

    def close_all(self, session: Session):
        session.close_all()