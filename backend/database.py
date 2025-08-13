from sqlalchemy import create_engine
<<<<<<< HEAD
from sqlalchemy.ext.declarative import declarative_base
=======
#from sqlalchemy.ext.declarative import declarative_base  A changer
from sqlalchemy.orm import declarative_base
>>>>>>> sara
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

<<<<<<< HEAD
=======

>>>>>>> sara
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

<<<<<<< HEAD
=======

>>>>>>> sara
# Dépendance FastAPI pour obtenir la session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
<<<<<<< HEAD
        db.close()
=======
        db.close()
>>>>>>> sara
