from fastapi import FastAPI
from app.routers.conversations import router as conversations_router

app = FastAPI()

app.include_router(conversations_router)
