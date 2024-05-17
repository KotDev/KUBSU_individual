from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///person.db")
sync_session = sessionmaker(bind=engine, expire_on_commit=False)
session = sync_session()
Base = declarative_base()