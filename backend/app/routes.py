from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def default():
    return {
        "message": "Welcome to e-com" 
    }

