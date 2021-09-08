import logging

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from startleft.api.api_config import ApiConfig
from startleft.api.controllers.cloudformation import cloudformation_controller
from startleft.api.controllers.health import health_controller
from startleft.api.error_response import ErrorResponse
from startleft.api.errors import IriusUnauthorizedError

webapp = FastAPI()
logger = logging.getLogger(__name__)

webapp.include_router(health_controller.router)
webapp.include_router(cloudformation_controller.router)


def initialize_webapp(iriusrisk_server: str):
    ApiConfig.set_iriusrisk_server(iriusrisk_server)

    return webapp


@webapp.exception_handler(IriusUnauthorizedError)
async def handle_irius_unauthorized_error(request: Request, e: IriusUnauthorizedError):
    return common_response_handler(
        401, 'Authentication information is missing or invalid or not granted to perform this action.')


@webapp.exception_handler(FileNotFoundError)
async def handle_file_not_found_error(request: Request, e: FileNotFoundError):
    return common_response_handler(404, 'File not found')


def common_response_handler(status_code: int, message: str):
    error_response = ErrorResponse(status='error', message=message)

    return JSONResponse(status_code=status_code, content=jsonable_encoder(error_response))
