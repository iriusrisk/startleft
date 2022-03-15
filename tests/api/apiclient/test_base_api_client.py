from unittest.mock import Mock, patch

import pytest
from requests import Response

from startleft.api.errors import IriusUnauthorizedError, IriusCommonApiError
from startleft.apiclient.base_api_client import BaseApiClient


class TestBaseApiClient:

    @patch('startleft.apiclient.base_api_client.requests.get')
    def test_check_response_api_error_response(self, mock_response):
        # Given a mocked unauthorized response
        mock_response.return_value.ok = False
        mock_response.return_value.status_code = 500

        # And an BaseApiClient
        base_api_client = BaseApiClient('example.com', 'abc-123')

        # When perform some operation
        # Then
        with pytest.raises(IriusCommonApiError):
            base_api_client.get("/path")

    @patch('startleft.apiclient.base_api_client.requests.get')
    def test_check_response_unauthorized_response(self, mock_response):
        # Given a mocked unauthorized response
        mock_response.return_value.ok = False
        mock_response.return_value.status_code = 401

        # And an BaseApiClient
        base_api_client = BaseApiClient('example.com', 'abc-123')

        # When perform some operation
        # Then
        with pytest.raises(IriusUnauthorizedError):
            base_api_client.get("/path")
