from fastapi import APIRouter

from .note_routes import router as note_router
from .user_routes import router as user_router

router = APIRouter()

@router.get("/", tags=["Home"])
async def home():
    return {"message": "It's working!"}

router.include_router(note_router)
router.include_router(user_router)
