from fastapi import APIRouter, status, Depends
from data_validation_schemas import SignUpSchema, LoginSchema
from db_helpers import Session, engine
from table_models import User
from fastapi.exceptions import HTTPException
from bcrypt import hashpw, checkpw, gensalt
from fastapi_jwt_auth import AuthJWT

session = Session(bind = engine)

auth_router = APIRouter(
    prefix = "/auth",
    tags = ['auth']
)

@auth_router.get('/', status_code = status.HTTP_200_OK)
async def home_page(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    return {"message" : f'Hello {Authorize.get_jwt_subject()}'}

@auth_router.post('/signup', status_code = status.HTTP_201_CREATED)
async def signup(user: SignUpSchema):
    db_email_check = session.query(User).filter(User.email == user.email).first()
    if db_email_check is not None:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "User with email already exists")

    new_user = User(full_name = user.full_name,
                    email = user.email,
                    password = hashpw(user.password.encode('utf-8'), gensalt()).decode('utf-8'),
                    is_staff = user.is_staff if user.is_staff else False,
                    is_active = user.is_active if user.is_active else True
                )
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@auth_router.post('/login', status_code = status.HTTP_200_OK)
async def login(user: LoginSchema, Authorize: AuthJWT = Depends()):
    db_user = session.query(User).filter(User.email == user.email).first()
    if db_user and checkpw(user.password.encode('utf-8'), db_user.password.encode('utf-8')):
        access_token = Authorize.create_access_token(subject = db_user.email)
        refresh_token = Authorize.create_refresh_token(subject = db_user.email)

        Authorize.set_access_cookies(access_token)
        Authorize.set_refresh_cookies(refresh_token)

        return {'message' : 'Successfully logged in'}
    raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,  
        detail = "User does not exist or invalid credentails"
    )


@auth_router.get('/refresh', status_code = status.HTTP_200_OK)
async def refresh_token(Authorize : AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Please provide a valid refresh token"
        ) 
    Authorize.set_access_cookies(Authorize.create_access_token(subject = Authorize.get_jwt_subject()))
    return {"message" : "Tokens refreshed"}

@auth_router.delete('/logout')
def logout(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except:
        raise HTTPException(status_code = status.HTTP_204_NO_CONTENT, detail = "You were never logged in")

    Authorize.unset_jwt_cookies()
    return {"message" : "Successfully logged out"}