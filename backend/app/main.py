from fastapi import FastAPI
from app.api.routes.auth import router as auth_router

from app.api.routes.conversations import router as conversation_router
from app.db.database import Base, engine
from app.models import *
from app.api.routes.users import router as users_router
from app.api.routes.messages import router as message_router
from app.websocket.websocket import router as websocket_router
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Signal Clone API",
    version="1.0.0",
)

app.include_router(users_router)
app.include_router(auth_router)
app.include_router(conversation_router)
app.include_router(message_router)
app.include_router(websocket_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://YOUR_PROJECT.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "Signal Clone Backend Running 🚀"
    }