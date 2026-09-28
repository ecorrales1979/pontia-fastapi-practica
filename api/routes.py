from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def home():
    return {"message": "It's working!"}
