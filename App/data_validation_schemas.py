import os
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field, constr, validator
from typing import Optional, List, Annotated

def get_secret_token():
    return os.environ.get("SECRET_TOKEN")

class Settings(BaseModel):
    authjwt_secret_key: Annotated[str, Field(default_factory = get_secret_token)]
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_csrf_protect: bool = False


class SignUpSchema(BaseModel):
    full_name: str
    email: str
    password: str
    is_staff: Optional[bool] = False
    is_active: Optional[bool] = True

    class Config:
        from_attributes = True
        json_schema_extra = {
            'example' : {
                'full_name' : 'johndoe',
                'email' : 'johndoe@some_app.com',
                'password' : 'password',
                'is_staff': False,
                'is_active' : True
            }
        }

class LoginSchema(BaseModel):
    email: str
    password: str
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example" : {
                "email" : "user_name@domain.dom_extension",
                "password" : "random_string"
            }
        }

class ItemSchema(BaseModel):
    pizza_name: str
    quantity: int

    class Config:
        json_schema_extra = {
            "pizza_name" : "Margherita",
            "quantity" : 2
        }

class AddressSchema(BaseModel):
    street: str
    city: Annotated[str, constr(max_length = 20)]
    state: Annotated[str, constr(max_length = 20)]
    country: Annotated[str, constr(max_length = 20)]
    zip_code: Annotated[str, constr(max_length = 20)]

    class Config:
        json_schema_extra = {
            "street" : "Street Address",
            "city" : "City Name",
            "state" : "State or State Code",
            "country" : "Country Name",
            "zip_code" : "postal code"
        }
    
class OrderSchema(BaseModel):
    order_date: Optional[datetime] = Field(default_factory = datetime.now)
    delivery_address: AddressSchema
    items: List[ItemSchema]

    class Config:
        json_schema_extra = {
            "order_date" : "2024-11-31T00:00:00",
            "delivery_address": {
                "street" : "Street Address",
                "city" : "City Name",
                "state" : "State or State Code",
                "country" : "Country Name",
                "zip_code" : "postal code"
            },

            "items" : [
                {'pizza_name' : "Corn and Cheese", 'quantity' : 2},
                {'pizza_name' : 'Margherita', 'quantity' : 1}
            ]
        }

    @validator("order_date", pre=True, always=True)
    def validate_order_date(cls, value):
        if value and value > datetime.now():
            raise ValueError("past_date must be in the past.")
        return value

class PizzaSize(str, Enum):
        SMALL = "small"
        MEDIUM = 'medium'
        LARGE = 'large'
        EXTRA_LARGE = 'extra-large'

class AddPizza(BaseModel):
    
    pizza_name: Annotated[str, Field(max_length = 30)]
    pizza_size: Optional[str]
    description: Optional[str]
    price: float
    
    class Config:
        json_schema_extra = {
            'example' : {
                'pizza_name' : 'Margherita',
                'pizza_size' : 'medium',
                'description' : 'Just cheese for the cheese lovers',
                'price' : 12.99
            }
        }

    @validator("pizza_size", pre=True, always=True)
    def validate_pizza_size(cls, value):
        if value and value.lower() not in PizzaSize.__members__.values():
            raise ValueError("Pizza size must be one of small, medium, large, extra-large")
        return value.lower()