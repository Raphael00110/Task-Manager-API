from fastapi import APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm
from services.user_service import *
from schemas.user import *



router = APIRouter() # as this is not the main app we have to route to the main file connection

# login
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
      return login_user(username=form_data.username,password=form_data.password)

# my account
@router.get("/me")
def get_me(current_user = Depends(get_current_user)):
      return current_user
# register
@router.post("/register", response_model=ViewUser, status_code=status.HTTP_201_CREATED)
def register_user(new_user: CreateUser):
      return create_user(new_user)

# search for a user
@router.get("/user", response_model=ViewUser)
def get_user(username: str):
      return get_user_by_username(username)




      
