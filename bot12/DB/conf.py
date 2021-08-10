from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
# from bot import DATABASE_URL, LOGGER
import os


def start() -> scoped_session:
  try:
    uri = os.getenv("DATABASE_URL")  # or other relevant config var
    if uri.startswith("postgres://"):
      uri = uri.replace("postgres://", "postgresql://", 1)
      
    engine = create_engine(uri)
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))
  except ValueError:
    print('Invalid DATABASE_URL : Exiting now.')
    exit(1)


BASE = declarative_base()
SESSION = start()