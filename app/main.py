from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from slowapi import Limiter
from slowapi.util import get_remote_address
import app.cloudinary_service
from app.database import Base
from app.database import engine

from app.routes import auth
from app.routes import contacts
from app.routes import users

Base.metadata.create_all(bind=engine)

app = FastAPI()

limiter = Limiter(
    key_func=get_remote_address
)

app.state.limiter = limiter

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)

app.include_router(contacts.router)

app.include_router(users.router)

@app.get("/")
def root():
    return {
        "message": "API works"
    }