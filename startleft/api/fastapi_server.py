from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from startleft.api.controllers.cloudformation import cloudformation_controller
from startleft.api.controllers.health import health_controller
from startleft.api.error_response import ErrorResponse

webapp = FastAPI()


def create_app():
    webapp.include_router(health_controller.router)
    webapp.include_router(cloudformation_controller.router)

    webapp.exception_handler(handle_file_not_found_error)

    return webapp


@webapp.exception_handler(FileNotFoundError)
async def handle_file_not_found_error(request: Request, e: FileNotFoundError):
    error_response = ErrorResponse(status=404, message_type="File not found")
    return common_response_handler(error_response)


def common_response_handler(error_response: ErrorResponse):
    json_compatible_item_data = jsonable_encoder(error_response)
    return JSONResponse(status_code=error_response.status, content=json_compatible_item_data)
