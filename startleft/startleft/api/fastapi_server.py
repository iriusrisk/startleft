import logging
from typing import Dict, Any, List

import uvicorn
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from startleft.startleft.api.controllers.diagram import diag_create_otm_controller
from startleft.startleft.api.controllers.etm import etm_create_otm_controller
from startleft.startleft.api.controllers.health import health_controller
from startleft.startleft.api.controllers.iac import iac_create_otm_controller
from startleft.startleft.api.error_response import ErrorResponse
from slp_base.slp_base.errors import CommonError
from startleft.startleft.log import VERBOSE_MESSAGE_FORMAT, get_uvicorn_log_level, set_log_level_from_uvicorn

webapp = FastAPI()
logger = logging.getLogger(__name__)
set_log_level_from_uvicorn()

webapp.include_router(health_controller.router)
webapp.include_router(iac_create_otm_controller.router)
webapp.include_router(diag_create_otm_controller.router)
webapp.include_router(etm_create_otm_controller.router)


def initialize_webapp():
    webapp.exception_handler(handle_common_error)
    webapp.exception_handler(handle_http_exception)
    webapp.exception_handler(handle_unexpected_exceptions)

    return webapp


def get_log_config():
    log_config = uvicorn.config.LOGGING_CONFIG
    app_log_level = get_uvicorn_log_level()
    log_config["loggers"]["uvicorn"]["level"] = app_log_level
    log_config["loggers"]["uvicorn.error"]["level"] = app_log_level
    log_config["loggers"]["uvicorn.access"]["level"] = app_log_level
    log_config["loggers"]["uvicorn"]["propagate"] = False
    log_config["formatters"]["access"]["fmt"] = VERBOSE_MESSAGE_FORMAT
    log_config["formatters"]["default"]["fmt"] = VERBOSE_MESSAGE_FORMAT

    return log_config


def run_webapp(port: int):
    uvicorn.run(webapp, host="127.0.0.1", port=port, log_config=get_log_config())


@webapp.exception_handler(HTTPException)
async def handle_http_exception(request: Request, httpe: HTTPException):
    logger.exception(httpe)
    title = httpe.detail if (hasattr(httpe, 'detail') and httpe.detail is not None) else 'Something went wrong handling the request'
    return common_response_handler(httpe.status_code, httpe.__class__.__name__, title, str(request.url), [])


@webapp.exception_handler(CommonError)
async def handle_common_error(request: Request, e: CommonError):
    logger.exception(e)
    return common_error_exception_handler(request, e)


@webapp.exception_handler(Exception)
async def handle_unexpected_exceptions(request: Request, e: Exception):
    logger.exception(e)
    message = e.message if hasattr(e, 'message') else str(e)
    return common_response_handler(500, e.__class__.__name__, 'Unexpected exception', '', [message])


@webapp.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.exception(exc)
    messages = []
    try:
        for error in exc.errors():
            messages.append(get_error(error))
    except Exception as e:
        logger.exception(e)
        messages = [str(exc.errors())]

    error_type = exc.__class__.__name__
    return common_response_handler(400, error_type, "The request is not valid", "InvalidRequest", messages)


def common_error_exception_handler(request: Request, exc: CommonError):
    message = exc.message
    detail = exc.detail
    title = exc.title
    http_status = exc.error_code.http_status
    return common_response_handler(http_status, exc.__class__.__name__, title, detail, [message])


def get_error(error: Dict[str, Any]) -> str:
    message = ''
    loc = error['loc']
    if loc:
        message = f'Error in field \'{loc[1]}\' located in \'{loc[0]}\'.'
    msg = error['msg']
    if msg:
        message = message + f' {msg}'

    return message


def common_response_handler(status_code: int, type_: str, title: str, detail: str, messages: List[str] = []):
    error_response = ErrorResponse(error_type=type_, status=status_code, title=title, detail=detail, messages=messages)

    return JSONResponse(status_code=status_code, content=jsonable_encoder(error_response))

