from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from models import User, Todo
from schemas import UserCreate, UserResponse, UserLoginResponse, TodoResponse, TodoCreate, UserLogin
from auth import hash_password, verify_password, create_access_token
from dependencies import get_current_user
from database import create_session
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/register", response_model = UserResponse, status_code=status.HTTP_201_CREATED, response_description = "User created")
def register(user_data : UserCreate, db : Session = Depends(create_session)):
    existing_object = db.query(User).filter(User.email == user_data.email).first()
    if existing_object is not None:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Email already exists")

    hashed_pwd = hash_password(user_data.password.get_secret_value())
    new_user = User(username = user_data.username, email = user_data.email, password = hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model = UserLoginResponse)
def login(user_data: UserLogin, db : Session = Depends(create_session)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if user is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Incorrect credentials")
    
    pwd_verify = verify_password(login_pwd = user_data.password.get_secret_value() , db_pwd = user.password)
    if not pwd_verify:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Incorrect credentials")
    token = create_access_token(user_id= user.id)
    login = UserLoginResponse(access_token=token, token_type = "bearer")
    return login