from fastapi import APIRouter
from startleft.api.api_config import ApiConfig
from fastapi.responses import JSONResponse

from startleft.apiclient.calls.is_healthy import IsHealthy

PREFIX = ''
URL = '/health'
RESPONSE_BODY_IRIUSRISK_OK = {"status": "OK", "components": {"StartLeft": "OK", "IriusRisk": "OK"}}
RESPONSE_BODY_IRIUSRISK_KO = {"status": "KO", "components": {"StartLeft": "OK", "IriusRisk": "KO"}}

router = APIRouter(prefix=PREFIX)


@router.get(URL, tags=["health"])
async def health():
    is_healthy = IsHealthy(ApiConfig.get_iriusrisk_server(), None)
    if is_healthy.do_call():
        return JSONResponse(status_code=200, content=RESPONSE_BODY_IRIUSRISK_OK)
    else:
        return JSONResponse(status_code=503, content=RESPONSE_BODY_IRIUSRISK_KO)
