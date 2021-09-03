import json
import logging
from http.client import HTTPException, NOT_FOUND

from startleft.api.errors import IriusTokenError, IriusServerError, IriusApiError
from startleft.api.flask_server import webapp

logger = logging.getLogger(__name__)


@webapp.errorhandler(FileNotFoundError)
def handle_file_not_found_error(e: FileNotFoundError):
    data = json.dumps({
        "code": NOT_FOUND,
        "name": e.strerror
    })
    return data, 404


@webapp.errorhandler(Exception)
def handle_exception(e):
    return common_handler(e)


@webapp.errorhandler(HTTPException)
def handle_http_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


@webapp.errorhandler(IriusTokenError)
def handle_irius_token_error(e: IriusTokenError):
    logger.log("IriusTokenError")
    return common_handler(e)


@webapp.errorhandler(IriusServerError)
def handle_irius_server_error(e: IriusServerError):
    logger.log("IriusServerError")
    return common_handler(e)


@webapp.errorhandler(IriusApiError)
def handle_irius_api_error(e: IriusApiError):
    return common_handler(e)


def common_handler(e):
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response
