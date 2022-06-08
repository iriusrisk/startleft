import logging
from typing import Dict, Any, List

import uvicorn
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from startleft.api.controllers.diagram import diag_create_otm_controller
from startleft.api.controllers.health import health_controller
from startleft.api.controllers.iac import iac_create_otm_controller
from startleft.api.error_response import ErrorResponse
from startleft.api.errors import CommonError, ErrorCode, MappingFileSchemaNotValidError, IacFileNotValidError, \
    DiagramFileNotValidError, ParsingError

webapp = FastAPI()
logger = logging.getLogger(__name__)

webapp.include_router(health_controller.router)
webapp.include_router(iac_create_otm_controller.router)
webapp.include_router(diag_create_otm_controller.router)


def initialize_webapp():
    webapp.exception_handler(handle_common_error)
    webapp.exception_handler(handle_unexpected_exceptions)

    return webapp


def run_webapp(port: int):
    uvicorn.run(webapp, host="127.0.0.1", port=port, log_level="info")


@webapp.exception_handler(CommonError)
async def handle_common_error(request: Request, e: CommonError):
    return common_response_handler(e.http_status_code, e.error_code, None, e.message)


@webapp.exception_handler(Exception)
async def handle_unexpected_exceptions(request: Request, e: Exception):
    message = e.message if hasattr(e, 'message') else str(e)
    error_code = ErrorCode.IAC_TO_OTM_EXIT_UNEXPECTED
    return common_response_handler(500, error_code.error_type, error_code.name, None, message)


@webapp.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc):
    messages = []
    try:
        for error in exc.errors():
            messages.append(get_error(error))
    except Exception as e:
        logger.exception(e)
        messages = [str(exc.errors())]

    error_type = ErrorCode.IAC_TO_OTM_EXIT_VALIDATION_FAILED.error_type
    return common_response_handler(400, error_type, "ValidationError", "RequestValidationError", messages)


@webapp.exception_handler(MappingFileSchemaNotValidError)
async def mapping_file_validation_exception_handler(request: Request, exc):
    message = exc.message
    from startleft import messages
    detail = messages.MAPPING_FILE_SCHEMA_NOT_VALID
    error_type = ErrorCode.MAPPING_FILE_EXIT_VALIDATION_FAILED.error_type
    return common_response_handler(400, error_type, 'MappingFileSchemaNotValidError', detail, [message])


@webapp.exception_handler(IacFileNotValidError)
async def iac_file_validation_exception_handler(request: Request, exc):
    return source_file_validation_exception_handler(request, exc)


@webapp.exception_handler(DiagramFileNotValidError)
async def diagram_file_validation_exception_handler(request: Request, exc):
    return source_file_validation_exception_handler(request, exc)


@webapp.exception_handler(ParsingError)
async def diagram_file_validation_exception_handler(request: Request, exc):
    return source_file_validation_exception_handler(request, exc)


def source_file_validation_exception_handler(request: Request, exc: CommonError):
    message = exc.message
    detail = exc.message
    error_type = exc.error_code.error_type
    return common_response_handler(400, error_type, exc.__class__.__name__, detail, [message])


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

    return JSONResponse(status_code=status_code,
                        content=jsonable_encoder(error_response))


