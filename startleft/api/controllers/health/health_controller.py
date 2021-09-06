from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["health"])
async def cloudformation():
    return "<p>StartLeft server is ok</p>"
