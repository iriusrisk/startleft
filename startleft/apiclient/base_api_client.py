import logging
from enum import Enum

from startleft.api.errors import IriusTokenNotSetError, IriusServerNotSetError, IriusCommonApiError, \
    IriusUnauthorizedError, IriusForbiddenError, IriusProjectNotFoundError

logger = logging.getLogger(__name__)


class IriusRiskApiVersion(Enum):
    v1 = "/api/v1"
    v2 = "/api/v2"


class BaseApiClient:

    def __init__(self, base_url, token):
        self.base_url = base_url
        self.token = token
        self.name = None
        self.id = None

    def headers(self):
        if not self.token:
            raise IriusTokenNotSetError
        return {"api-token": "{}".format(self.token)}

    def irius_v1_url(self, path):
        return self.__irius_url(path, IriusRiskApiVersion.v1)

    def __irius_url(self, path, api_version: IriusRiskApiVersion):
        if not self.base_url:
            raise IriusServerNotSetError
        return self.base_url + api_version.value + path

    def check_response(self, response):
        if response.status_code == 401:
            raise IriusUnauthorizedError(self.get_error_message(response))
        if response.status_code == 403:
            raise IriusForbiddenError(self.get_error_message(response))
        if response.status_code == 404:
            raise IriusProjectNotFoundError(self.get_error_message(response))
        if not response.ok:
            raise IriusCommonApiError(http_status_code=response.status_code, message=response.text)
        logger.debug(f"Response received {response.status_code}: {response.text}")

    def get_error_message(self, response):
        return f"API return an unexpected response: {response.status_code}\n" \
               f"Response url: {response.url}\n" \
               f"Response body:{response.text}"

    def open_file(self, otm_file):
        if isinstance(otm_file, tuple):
            files = {"file": open(otm_file[0], 'rb')}
        else:
            files = {"file": open(otm_file, 'rb')}

        return files
