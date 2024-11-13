from fastapi import APIRouter, status
from data_validation_schemas import SignUp
from db_helpers import Session, engine
from table_models import User
from fastapi.exceptions import HTTPException
from bcrypt import hashpw, checkpw, gensalt

session = Session(bind = engine)

auth_router = APIRouter(
    prefix = "/auth",
    tags = ['auth']
)

@auth_router.get('/')
async def hello():
    return {"message" : 'Hello World'}

@auth_router.post('/signup', status_code = status.HTTP_201_CREATED)
async def signup(user: SignUp):
    db_email_check = session.query(User).filter(User.email == user.email).first()
    if db_email_check is not None:
        return HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "User with email already exists")

    new_user = User(full_name = user.full_name,
                    email = user.email,
                    password = hashpw(user.password.encode('utf-8'), gensalt())
                )
    
    session.add(new_user)
    session.commit()
    return new_user