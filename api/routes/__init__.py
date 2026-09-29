from fastapi import APIRouter

from .note_routes import router as note_router

router = APIRouter()

@router.get("/", tags=["Home"])
async def home():
    return {"message": "It's working!"}

router.include_router(note_router)
