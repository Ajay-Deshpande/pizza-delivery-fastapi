from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from data_validation_schemas import AddPizza
from table_models import Pizza, User
from db_helpers import Session, engine

session = Session(bind = engine)

pizza_router = APIRouter(
        prefix = '/pizza',
        tags = ['pizza']
    )

def check_user_role(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                            detail = "Not authorized to add Pizza to Menu. Please sign in with Staff Account"
                )
    user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.email == user).first()
    return user.is_staff

@pizza_router.post('/add_pizza')
async def add_pizza_to_menu(pizza: AddPizza, Authorize: AuthJWT = Depends(), is_staff = Depends(check_user_role)):
    try:
        Authorize.jwt_required()
    except:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, 
                            detail = "Not authorized to add Pizza to Menu. Please sign in with Staff Account"
                    )
    if not is_staff:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                            detail = "Not authorized to add Pizza to Menu. Please sign in with Staff Account"
                    )
    print("1")
    new_pizza = Pizza(pizza_name = pizza.pizza_name,
                      description = pizza.description if pizza.description else "",
                      pizza_size = pizza.pizza_size,
                      price = pizza.price)
    
    session.add(new_pizza)
    session.commit()
    return {'message' : f"Successfully added {pizza.pizza_name} pizza to menu"}
