from fastapi import APIRouter
from startleft.api.api_config import ApiConfig

router = APIRouter()


@router.get("/health", tags=["health"])
async def health():
    return {"status": "StartLeft server is ok"}


@router.get("/health2", tags=["health"])
async def health2():
    return ApiConfig.get_iriusrisk_server()
