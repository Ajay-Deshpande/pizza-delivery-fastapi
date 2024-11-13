from pydantic import BaseModel
from typing import Optional

class SignUp(BaseModel):
    # user_id: Optional[int]
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
