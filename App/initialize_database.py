from db_helpers import Base, engine, Session
from table_models import User, Order, OrderItems, Pizza, Address

try:
    session = Session()
    Base.metadata.create_all(engine)
    session.commit()
except Exception as e:
    print("Unable to create tables")
    print(e)
    
