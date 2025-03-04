from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import engine, Base
from app.api.v1.routes import users

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up... Running DB migrations")
    Base.metadata.create_all(bind=engine)
    yield
    print("Shutting down... Closing connections")

app = FastAPI(title="FastAPI Scaffold", lifespan=lifespan)
app.include_router(users.router, prefix="/users", tags=["Users"])

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Scaffold"}
