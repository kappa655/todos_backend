from typing import List
from schemas import TodoUpdate, TodoResponse, TodoCreate
from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from database import create_session
from models import User, Todo
from dependencies import get_current_user

router = APIRouter()

@router.post("/create_todo", response_model = TodoResponse)
def create_todo(user_data : TodoCreate, db : Session = Depends(create_session),
                user : User = Depends(get_current_user)):
    todo = Todo(title = user_data.title, description = user_data.description, owner_id = user.id)
    db.add(todo)
    db.commit()
    db.refresh(todo)

    return todo

@router.get("/todos", response_model = List[TodoResponse], status_code = status.HTTP_200_OK)
def get_todos(db : Session = Depends(create_session), user : User = Depends(get_current_user)):
    user_todos = db.query(Todo).filter(Todo.owner_id == user.id).all()
    return user_todos

@router.get("/todos/{todo_id}", response_model = TodoResponse)
def get_todo(todo_id : int, db : Session = Depends(create_session), user : User = Depends(get_current_user)):
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.owner_id == user.id).first()
    if todo is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= "Todo not found")
    return todo

@router.patch("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(user_data : TodoUpdate, todo_id : int, db : Session = Depends(create_session),
                 user : User = Depends(get_current_user)):
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.owner_id == user.id).first()
    if todo is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= "Todo not found")
    update_data = user_data.model_dump(exclude_unset = True)
    for key, value in update_data.items():
        setattr(todo, key, value)

    db.commit()
    db.refresh(todo)
    return todo

@router.delete("/todos/{todo_id}")
def delete_todo(todo_id : int, db : Session = Depends(create_session), user : User = Depends(get_current_user)):
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.owner_id == user.id).first()
    if todo is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= "Todo not found")
    db.delete(todo)
    db.commit()
    return {"message" : "Todo deleted successfully"}