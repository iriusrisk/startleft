import logging
from typing import Dict, Any, List

import uvicorn
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from startleft.api.api_config import ApiConfig
from startleft.api.controllers.diagram import diag_create_otm_controller
from startleft.api.controllers.iac import iac_create_otm_controller
from startleft.api.controllers.health import health_controller
from startleft.api.error_response import ErrorResponse
from startleft.api.errors import CommonError

webapp = FastAPI()
logger = logging.getLogger(__name__)

webapp.include_router(health_controller.router)
webapp.include_router(iac_create_otm_controller.router)
webapp.include_router(diag_create_otm_controller.router)


def initialize_webapp(iriusrisk_server: str):
    ApiConfig.set_iriusrisk_server(iriusrisk_server)

    webapp.exception_handler(handle_common_error)
    webapp.exception_handler(handle_unexpected_exceptions)

    return webapp


def run_webapp(port: int):
    uvicorn.run(webapp, host="127.0.0.1", port=port, log_level="info")


@webapp.exception_handler(CommonError)
async def handle_common_error(request: Request, e: CommonError):
    return common_response_handler(e.http_status_code, [e.message])


@webapp.exception_handler(Exception)
async def handle_unexpected_exceptions(request: Request, e: Exception):
    message = e.message if hasattr(e, 'message') else str(e)
    return common_response_handler(500, [message])


@webapp.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc):
    messages = []
    try:
        for error in exc.errors():
            messages.append(get_error(error))
    except Exception as e:
        logger.exception(e)
        messages = [str(exc.errors())]

    return common_response_handler(400, messages)


def get_error(error: Dict[str, Any]) -> str:
    message = ''
    loc = error['loc']
    if loc:
        message = f'Error in field \'{loc[1]}\' located in \'{loc[0]}\'.'
    msg = error['msg']
    if msg:
        message = message + f' {msg}'

    return message


def common_response_handler(status_code: int, messages: List[str]):
    error_response = ErrorResponse(status='error', messages=messages)

    return JSONResponse(status_code=status_code, content=jsonable_encoder(error_response))
