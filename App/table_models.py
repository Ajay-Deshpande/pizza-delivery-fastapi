from db_helpers import Base
from sqlalchemy import Column, Integer, Boolean, Text, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType

class User(Base):
    __tablename__ = 'User'
    user_id = Column(Integer, primary_key = True, autoincrement = True)
    full_name = Column(String(25))
    email = Column(String(80), unique = True)
    password = Column(Text, nullable = True)
    is_staff = Column(Boolean, default = False)
    is_active = Column(Boolean, default = False)
    orders = relationship('Order', back_populates = 'User')

    def __repr__(self):
        return f"<User {self.full_name}"

class Address(Base):
    __tablename__ = "Address"
    address_id = Column(Integer, autoincrement = True, primary_key = True)
    street = Column(Text)
    city = Column(String(20))
    state = Column(String(20))
    country = Column(String(20))
    zip_code = Column(String(20))
    orders = relationship('Order', back_populates = 'Address')

class Pizza(Base):

    PIZZA_SIZES=(
        ('SMALL','small'),
        ('MEDIUM','medium'),
        ('LARGE','large'),
        ('EXTRA-LARGE','extra-large')
    )

    __tablename__ = "Pizza"
    pizza_id = Column(Integer, primary_key = True, autoincrement = True)
    pizza_name = Column(String(30))
    pizza_size = Column(ChoiceType(choices = PIZZA_SIZES), default = "SMALL")
    description = Column(Text, nullable = True)
    price = Column(Integer)
    
    def __repr__(self):
        return f"{self.description}"

class Order(Base):

    ORDER_STATUSES=(
        ('PENDING','pending'),
        ("ORDER-ACCEPTED", "order-accepted"),
        ('IN-TRANSIT','in-transit'),
        ('DELIVERED','delivered')
    )

    PAYMENT_STATUS = (
        ('PAID-BY-CARD', 'paid-by-card'),
        ('PAID-BY-CASH', 'paid-by-cash'),
        ("PENDING-PAYMENT", "pending-payment")
    )

    __tablename__='Orders'
    order_id = Column(Integer, primary_key = True, autoincrement = True)
    order_status = Column(ChoiceType(choices = ORDER_STATUSES), default="PENDING")
    user_id = Column(Integer, ForeignKey('User.user_id'))
    order_amount = Column(Integer)
    payment_status = Column(ChoiceType(choices = PAYMENT_STATUS), default = "PENDING-PAYMENT")
    order_date = Column(DateTime)
    deliver_address = Column(Integer, ForeignKey('Address.address_id'))
    user = relationship('User', back_populates='Orders')

    def __repr__(self):
        return f"<Order {self.order_id}>"
    
class OrderItems(Base):
    
    __tablename__ = "OrderItems"
    order_item_id = Column(Integer, primary_key = True, autoincrement = True)
    order_id = Column(Integer, ForeignKey('Orders.order_id'))
    pizza_id = Column(Integer, ForeignKey("Pizza.pizza_id"))
    quantity = Column(Integer)
    
    order = relationship('Order', back_populates='items')
    pizza = relationship('Pizza')
    
    def __repr__(self):
        return f"{self.quantity} {self.pizza_id}'s ordered"
