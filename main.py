from fastapi import FastAPI
from database import engine, Base
from routers.users import router as users_router
from routers.todos import router as todos_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

Base.metadata.create_all(bind = engine)
app.include_router(users_router)
app.include_router(todos_router)












    