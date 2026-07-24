from pwdlib import PasswordHash
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os   

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

password_hash = PasswordHash.recommended()
def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(login_pwd : str, db_pwd : str):
    pwd_verify = password_hash.verify(login_pwd, db_pwd)
    return pwd_verify

def create_access_token(user_id : int) :
    expire = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub" : str(user_id), "exp" : expire}
    encoded_jwt = jwt.encode(claims = payload,key = SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt
def decode_token(token : str) :
    try :
        payload = jwt.decode(token = token, key = SECRET_KEY, algorithms = [ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        else:
            return int(user_id)
    except JWTError:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

