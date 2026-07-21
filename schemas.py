from pydantic import BaseModel, EmailStr, Field, SecretStr

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: SecretStr = Field(..., min_length=8)
    email: EmailStr

class UserResponse(BaseModel):
    id : int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: SecretStr = Field(..., min_length=8)

class UserLoginResponse(BaseModel):
    access_token : str
    token_type : str

class TodoCreate(BaseModel):
    title : str = Field(..., min_length = 1, max_length = 100)
    description: str | None = None

class TodoUpdate(BaseModel):
    title : str | None = None
    description: str | None = None
    completed : bool | None = None

class TodoResponse(BaseModel):
    id : int
    title : str
    description: str | None = None
    completed : bool = False

    class Config:
        from_attributes = True
