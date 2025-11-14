import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api import auth as auth_router
from app.api import users as users_router
from app.api import portfolio
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Приложение запускается...")
    yield
    print("Приложение останавливается...")


app = FastAPI(title="AI Portfolio Builder API", lifespan=lifespan)

allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(portfolio.router)
app.include_router(auth_router.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(users_router.router, prefix="/api/v1/users", tags=["Users"])


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI Backend!"}


@app.get("/api/v1/test")
def read_test_endpoint():
    return {"data": "API v1 is working"}
