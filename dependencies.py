from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from database import create_session
from sqlalchemy.orm import  Session
from auth import decode_token
from models import User


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login"
)
def get_current_user(token : str = Depends(oauth2_scheme), db : Session = Depends(create_session)):
    user_id = decode_token(token)
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user
