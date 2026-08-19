from fastapi import HTTPException, status, Depends, Security
from schemas.user import *
from repositories import user_repository as u
from security import *
from Database.oauth_config import *


def create_user(new_user: CreateUser):
        user_exists = u.get_user_by_username(new_user.username)
        email_exists = u.get_user_by_email(new_user.email)
        if user_exists:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail=f"Username already exists!")
        if email_exists:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail=f"Email already exists")
        user = new_user.model_dump()
        user["password"] = hash_password(user["password"])
        
        return u.create_user(user)

def get_user_by_username(username: str):
        result = u.get_user_by_username(username)
        if not result:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                    detail=f"User with username {username} not found!")
        return result

def get_user_by_email(email: str):
        result = u.get_user_by_email(email)
        if not result:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"User with email {email} not found!")
        return result

def login_user(username: str, password: str):
        user = u.get_user_credentials(username) # we get the user credentials if user is present
        dummy_hash = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGGa31Sg" # create dummy hash for security 
        password_hash = user["password"] if user else dummy_hash # if user exist then good else store the dummy hash in password hash so it takes the same amount of check time this prevents timing attack
        valid_password = verify_password(password, password_hash) # verify password 
        if not user or not valid_password: # it user or pass is incorrect raise an exception
                raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail=f"Invalid Username or Password!")
        token = create_access_token({"username": user["username"]}) # create the access token by passing in the user credentials

        return { 
                "access_token": token,
                "token_type": "bearer"
        }




def get_current_user(token: str = Security(oauth2_scheme)):  # make the token parameter which takes the argument oauth2_scheme which has the access token
      credentials_exception = HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Could not verify credentials",
                headers= {"WWW-Autheticate": "Bearer"})

        
      try:
         decode_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # decode the token pass the token, secret key, and the algorithm
         sub = decode_data.get("sub") # extract and store the "sub" username from decoded token
         if sub is None: # if sub doesnt exist raise error
                raise credentials_exception
      except JWTError: # if there is a decoding or any jwt error
             raise credentials_exception

      find = u.get_user_by_username(sub) # find the username in database
      if not find: # if user doesnt exist
             raise credentials_exception
      return find

def get_current_user_id(current_user = Depends(get_current_user)):
       return current_user["id"] # this gets the current user's id




        




