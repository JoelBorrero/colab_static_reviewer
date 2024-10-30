from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.conversations import router as conversations_router
from app.routers.gpt import router as gpt_router


app = FastAPI()

app.include_router(conversations_router)
app.include_router(gpt_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
