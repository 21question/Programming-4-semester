from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlmodel import SQLModel


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)

    yield  # Здесь работает приложение

    # Shutdown code (если нужен)
    print("Shutting down...")


app = FastAPI(lifespan=lifespan)