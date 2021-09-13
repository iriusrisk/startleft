from fastapi import APIRouter
from startleft.api.api_config import ApiConfig

PREFIX = ''
URL = '/health'
RESPONSE_BODY = {"status": "StartLeft server is ok"}

router = APIRouter(prefix=PREFIX)


@router.get(URL, tags=["health"])
async def health():
    return RESPONSE_BODY


@router.get("/health2", tags=["health"])
async def health2():
    return ApiConfig.get_iriusrisk_server()
