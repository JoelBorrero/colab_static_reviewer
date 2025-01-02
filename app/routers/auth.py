from fastapi import APIRouter

from app.models import LoginRequest, LogoutRequest


router = APIRouter(prefix="/auth")

@router.post("/login")
async def login(request: LoginRequest):
    pass

@router.post("/logout")
async def logout(request: LogoutRequest):
    pass
