import os
from dotenv import load_dotenv
from pathlib import Path
from fastapi.security import OAuth2PasswordBearer


CURRENT_DIR = Path(__file__).resolve().parent
env_path = CURRENT_DIR.parent / ".env"
load_dotenv(dotenv_path=env_path)

SECRET_KEY = os.getenv("SECRET_KEY") # this is like the server's password which you have to pass to get access token or it is passed with a refresh token to get access token again also to prevent third party server's from trying to send requests etc
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") # verify username and password in login url if true pass the fetch the access token