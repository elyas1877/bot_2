from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
# from bot import DATABASE_URL, LOGGER


def start() -> scoped_session:
  try:
    engine = create_engine('postgresql://wfjhajuqtgqoas:c42d169cacfc005ef1d88eae9c674423d57ba535c2aafeecf77ef7f7ad93b699@ec2-3-226-134-153.compute-1.amazonaws.com:5432/d9leiaac4kshrh')
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))
  except ValueError:
    print('Invalid DATABASE_URL : Exiting now.')
    exit(1)


BASE = declarative_base()
SESSION = start()