from typing import Optional
from pydantic import Field, BaseModel, EmailStr



class CreateUser(BaseModel): # Model to create a new user includes field to specify the user input Optional and also specify datatype
    id: Optional[int] = Field(default=None, gt=0, description="Auto Generated ID")
    email: EmailStr = Field(min_length=5, max_length=255)
    username: str = Field(min_length=4, max_length=15)
    password: str = Field(min_length=6, max_length=20)

class ViewUser(BaseModel): # Model to view or display the user controlled details data type is passed before hand
    id: int
    username: str
    email: str
