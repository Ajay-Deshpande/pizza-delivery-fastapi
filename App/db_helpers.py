from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("postgresql+psycopg2://postgres:admin@postgres:5432/pizza_store", echo = True)

if not database_exists(engine.url):
    create_database(engine.url)
    print(f"Database {engine.url} created")

Base = declarative_base()

Session = sessionmaker()