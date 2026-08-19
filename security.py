from pwdlib import PasswordHash
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from Database.oauth_config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES




password_hash = PasswordHash.recommended() # initiate hash type recommended and assign it to a variable

def hash_password(password: str):  # create function return the password has of the str password 
    return password_hash.hash(password)

def verify_password(password: str, hashed_password:str): # created function add parameters password and the hashed_password and verify it returns T or F
    return password_hash.verify(password, hashed_password)

def create_access_token(data: dict):

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) # we add current time to timdelta + 30 mins as expiration time
    payload = {
        "exp":  expire,
        "sub":  str (data["username"])
    }# let payload sub be the username inside data and expiration time

    

    
    return jwt.encode( # at the end return the passed in payload, special key, and jwt algorithm of choice
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM)
    

