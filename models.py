from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from database import Base




class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    username = Column(String(50), nullable = False)
    email = Column(String(50), nullable = False)
    password =  Column(String(200), nullable = False)
    created_at =  Column(DateTime, server_default=func.now(), nullable = False)
    todos = relationship("Todo", back_populates = "owner")

    
class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key = True)
    title = Column(String(200), nullable = False)
    description = Column(String(200))
    completed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete = "CASCADE"), nullable = False)
    owner = relationship("User", back_populates = "todos")