from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
DB_URL = DB_URL = os.getenv("DB_URL")
engine = create_engine("mysql+pymysql://avnadmin:AVNS_yBm5abDexKF2ThjVx_z@tcc-g06-ecm-2024-tcc-transporte-escolar.l.aivencloud.com:24617/tcc-g06", echo=True)
SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()