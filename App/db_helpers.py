from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("postgresql+psycopg2://postgres:admin@localhost:5432/pizza_store", echo = True)
print(engine)
if not database_exists(engine.url):
    create_database(engine.url)

Base = declarative_base()

Session = sessionmaker()