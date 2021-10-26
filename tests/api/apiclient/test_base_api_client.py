import pytest
from requests import Response

from startleft.api.errors import IriusUnauthorizedError, IriusCommonApiError
from startleft.apiclient.base_api_client import BaseApiClient


class TestBaseApiClient:

    def test_check_response_unauthorized_response(self):
        # Given a response with status 401
        response = Response()
        response.status_code = 401

        # And an IriusRisk object
        base_api_client = BaseApiClient('example.com', 'abc-123')

        # When check_response, then exception is raised
        with pytest.raises(IriusUnauthorizedError):
            base_api_client.check_response(response)

    def test_check_response_api_error_response(self):
        # Given a response with error status not controlled
        response = Response()
        response.status_code = 500

        # And an IriusRisk object
        base_api_client = BaseApiClient('example.com', 'abc-123')

        # When check_response, then exception is raised
        with pytest.raises(IriusCommonApiError):
            base_api_client.check_response(response)
