from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from data_validation_schemas import OrderSchema, AddressSchema, ItemSchema
from table_models import Order, OrderItems, Address, User, Pizza
from db_helpers import Session, engine

session = Session(bind = engine)

order_router = APIRouter(
        prefix = "/orders",
        tags = ['orders']
    )

@order_router.post('/create_order')
async def create_order(order: OrderSchema, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                            detail = "Not authorized to create an order. Please sign in")
    new_address = Address(
                        street = order.delivery_address.street,
                        city = order.delivery_address.city,
                        state = order.delivery_address.state,
                        country = order.delivery_address.country,
                        zip_code = order.delivery_address.zip_code
                    )
    session.add(new_address)
    session.commit()
    session.refresh(new_address)
    
    user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.email == user).first()
    
    amount = 0

    for item in order.items:
        pizza = session.query(Pizza).filter(Pizza.pizza_name == item.pizza_name).first()
        amount += (item.quantity * pizza.price)
    
    new_order = Order(user_id = user.user_id, 
                      order_amount = amount, 
                      delivery_address = new_address.address_id,
                    )
    
    session.add(new_order)
    session.commit()
    session.refresh(new_order)

    for item in order.items:
        pizza = session.query(Pizza).filter(Pizza.pizza_name == item.pizza_name).first()
        new_item = OrderItems(order_id = new_order.order_id, pizza_id = pizza.pizza_id, quantity = item.quantity)
        session.add(new_item)
    session.commit()

    return {"message" : 'Hello World'}
