from fastapi import APIRouter
from fastapi.responses import JSONResponse

from _version.version_loader import load_startleft_version

PREFIX = ''
URL = '/health'
RESPONSE_BODY_STARTLEFT_OK = {"status": "OK", "version": load_startleft_version(), "components": {"StartLeft": "OK"}}

router = APIRouter(prefix=PREFIX)


@router.get(URL, tags=["health"])
async def health():
    return JSONResponse(status_code=200, content=RESPONSE_BODY_STARTLEFT_OK)
