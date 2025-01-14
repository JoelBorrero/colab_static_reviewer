from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.conversations import router as conversations_router
from app.routers.google_drive import router as google_drive_router
from app.routers.llm import router as llm_router


app = FastAPI()

app.include_router(conversations_router)
app.include_router(google_drive_router)
app.include_router(llm_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
