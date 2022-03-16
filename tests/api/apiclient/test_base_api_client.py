import json
from unittest.mock import patch

import pytest

from startleft.api.errors import IriusUnauthorizedError, IriusCommonApiError, IriusServerUnreachableError, \
    IriusProjectNotFoundError
from startleft.apiclient.base_api_client import BaseApiClient

API_SERVER_URL = 'http://no-ip:9999'
API_TOKEN = 'some-no-valid-token'


def set_response_ok(response, response_value=None):
    response.return_value.ok = True
    response.return_value.status_code = 200
    if response_value:
        response.return_value.json = lambda: response_value

    return response


class TestBaseApiClient:

    def test_iriusrisk_server_unreachable(self):
        # Given a BaseApiClient point to an invalid URL
        base_api_client = BaseApiClient(API_SERVER_URL, API_TOKEN)

        # When perform some operation
        # Then raise IriusServerUnreachableError
        with pytest.raises(IriusServerUnreachableError):
            base_api_client.get("/path")

    @patch('startleft.apiclient.base_api_client.requests.get')
    def test_check_response_unauthorized_response(self, mock_response):
        # Given a mocked unauthorized response
        mock_response.return_value.ok = False
        mock_response.return_value.status_code = 401

        # And a BaseApiClient
        base_api_client = BaseApiClient(API_SERVER_URL, API_TOKEN)

        # When perform some operation
        # Then raise IriusUnauthorizedError
        with pytest.raises(IriusUnauthorizedError):
            base_api_client.get("/path")
        assert mock_response.call_count == 1

    @patch('startleft.apiclient.base_api_client.requests.get')
    def test_generic_api_error_response_is_propagated(self, mock_response):
        # Given some API error status
        error_status = 'error_status'

        # And some API error response
        error_message = 'Error message from API'

        # And a mocked bad request response
        mock_response.return_value.ok = False
        mock_response.return_value.status_code = 400
        mock_response.return_value.json = lambda: dict(
            {'status': error_status, 'errors': [{'message': error_message}]})

        # And a BaseApiClient
        base_api_client = BaseApiClient(API_SERVER_URL, API_TOKEN)

        # When perform some operation
        # Then raise IriusCommonApiError with received message
        with pytest.raises(IriusCommonApiError) as api_error:
            base_api_client.get("/path")

        # And error message from API is propagated
        assert api_error.value.message == error_message
        assert mock_response.call_count == 1

    @patch('startleft.apiclient.base_api_client.requests.put')
    def test_irius_project_not_found_error(self, mock_response):
        # Given a mocked API not found response
        mock_response.return_value.ok = False
        mock_response.return_value.status_code = 404

        # And a BaseApiClient
        base_api_client = BaseApiClient(API_SERVER_URL, API_TOKEN)

        # When perform some operation
        # Then raise IriusProjectNotFoundError
        with pytest.raises(IriusProjectNotFoundError):
            base_api_client.put("/path")
        assert mock_response.call_count == 1

    @patch('startleft.apiclient.base_api_client.requests.get')
    def test_get_returns_api_response_ok(self, mock_response):
        # Given a valid API return value
        api_response_value = {'field': 'value'}

        # And a mocked OK response
        set_response_ok(mock_response, api_response_value)

        # And a BaseApiClient
        base_api_client = BaseApiClient(API_SERVER_URL, API_TOKEN)

        # When perform a GET operation
        response = base_api_client.get("/path")

        # Then API response is propagated
        assert api_response_value == response
        assert mock_response.call_count == 1

    @patch('startleft.apiclient.base_api_client.requests.post')
    def test_post_returns_api_response_ok(self, mock_response):
        # Given a valid API return value
        api_response_value = {'field': 'value'}

        # And a mocked OK response
        set_response_ok(mock_response, api_response_value)

        # And a BaseApiClient
        base_api_client = BaseApiClient(API_SERVER_URL, API_TOKEN)

        # When perform a POST operation
        response = base_api_client.post("/path")

        # Then API response is propagated
        assert api_response_value == response
        assert mock_response.call_count == 1

    @patch('startleft.apiclient.base_api_client.requests.put')
    def test_put_returns_api_response_ok(self, mock_response):
        # Given a valid API return value
        api_response_value = {'field': 'value'}

        # And a mocked OK response
        set_response_ok(mock_response, api_response_value)

        # And a BaseApiClient
        base_api_client = BaseApiClient(API_SERVER_URL, API_TOKEN)

        # When perform a PUT operation
        response = base_api_client.put("/path")

        # Then API response is propagated
        assert api_response_value == response
        assert mock_response.call_count == 1

    @patch('startleft.apiclient.base_api_client.requests.delete')
    def test_delete_calls_api(self, mock_response):
        # And a mocked OK response
        set_response_ok(mock_response)

        # And a BaseApiClient
        base_api_client = BaseApiClient(API_SERVER_URL, API_TOKEN)

        # When perform some operation
        base_api_client.delete("/path")

        # Then mocked API delete is called
        assert mock_response.call_count == 1

