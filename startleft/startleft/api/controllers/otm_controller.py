from http import HTTPStatus

from startleft.startleft import messages
from startleft.startleft.api.error_response import ErrorResponse

controller_responses = {
    201: {"description": messages.OTM_SUCCESSFULLY_CREATED},
    400: {"description": messages.BAD_REQUEST,
          "model": ErrorResponse},
    401: {"description": messages.UNAUTHORIZED_EXCEPTION,
          "model": ErrorResponse},
    403: {"description": messages.FORBIDDEN_OPERATION,
          "model": ErrorResponse},
    'default': {"description": messages.UNEXPECTED_API_ERROR,
                "model": ErrorResponse}
}

PREFIX = '/api/v1/startleft'

RESPONSE_STATUS_CODE = HTTPStatus.CREATED
