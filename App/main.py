from fastapi import FastAPI
from authentication_routes import auth_router
from orders_route import order_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(order_router)