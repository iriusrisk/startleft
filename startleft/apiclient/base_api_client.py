import logging
from enum import Enum

import requests

from startleft.api.errors import IriusTokenNotSetError, IriusServerNotSetError, IriusCommonApiError, \
    IriusUnauthorizedError, IriusForbiddenError, IriusProjectNotFoundError, IriusServerUnreachable

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

    def get(self, resource_path: str, headers: str = None):
        return self.__execute_request(requests.get, resource_path, headers)

    def post(self, resource_path: str, headers: str = None, file=None):
        return self.__execute_request(requests.post, resource_path, headers, file)

    def put(self, resource_path: str, headers: str = None, file=None):
        return self.__execute_request(requests.put, resource_path, headers, file)

    def delete(self, resource_path: str, headers: str = None):
        self.__execute_request(requests.delete, resource_path, headers)

    def _build_token_header(self):
        if not self.token:
            raise IriusTokenNotSetError
        return {"api-token": "{}".format(self.token)}

    def __execute_request(self, request_api, resource_path: str, headers: str = None, file=None):
        opened_file = self.__open_file(file) if file else None
        try:
            response = request_api(self.__irius_v1_url(resource_path), headers=headers, files=opened_file)

            self.__check_response(response)
            return response
        except ConnectionError:
            raise IriusServerUnreachable

    def __irius_v1_url(self, path):
        return self.__irius_url(path, IriusRiskApiVersion.v1)

    def __irius_url(self, path, api_version: IriusRiskApiVersion):
        if not self.base_url:
            raise IriusServerNotSetError
        return self.base_url + api_version.value + path

    def __check_response(self, response):
        if response.status_code == 401:
            raise IriusUnauthorizedError(self.__get_error_message(response))
        if response.status_code == 403:
            raise IriusForbiddenError(self.__get_error_message(response))
        if response.status_code == 404:
            raise IriusProjectNotFoundError(self.__get_error_message(response))
        if not response.ok:
            raise IriusCommonApiError(http_status_code=response.status_code, message=response.text)
        logger.debug(f"Response received {response.status_code}: {response.text}")

    def __get_error_message(self, response):
        return f"API return an unexpected response: {response.status_code}\n" \
               f"Response url: {response.url}\n" \
               f"Response body:{response.text}"

    def __open_file(self, file):
        if isinstance(file, tuple):
            files = {"file": open(file[0], 'rb')}
        else:
            files = {"file": open(file, 'rb')}

        return files
