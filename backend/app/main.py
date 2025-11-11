from fastapi import FastAPI
from contextlib import asynccontextmanager
from .db import create_db_and_tables 
from app.api import auth as auth_router
from app.api import users as users_router
from app.api import portfolio


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Приложение запускается...")
    yield
    print("Приложение останавливается...")

app = FastAPI(
    title="AI Portfolio Builder API",
    lifespan=lifespan 
)

app.include_router(portfolio.router)

app.include_router(
    auth_router.router, 
    prefix="/api/v1/auth",  
    tags=["Auth"]           
)

app.include_router(
    auth_router.router, 
    prefix="/api/v1/auth",
    tags=["Auth"]
)

app.include_router(
    users_router.router,
    prefix="/api/v1/users",
    tags=["Users"]
)


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI Backend!"}

@app.get("/api/v1/test")
def read_test_endpoint():
    return {"data": "API v1 is working"}