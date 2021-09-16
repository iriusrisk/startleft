from json import JSONDecodeError
from unittest.mock import Mock, patch, MagicMock

import pytest
from requests import Response

from startleft import iriusrisk


class TestIriusRisk:

    def test_check_response_unauthorized_response(self):
        # Given a response with status 401
        response = Response()
        response.status_code = 401

        # And an IriusRisk object
        ir = iriusrisk.IriusRisk('example.com', 'abc-123')

        # When check_response, then exception is raised
        with pytest.raises(iriusrisk.IriusUnauthorizedError):
            ir.check_response(response)

    def test_check_response_api_error_response(self):
        # Given a response with error status not controlled
        response = Response()
        response.status_code = 500

        # And an IriusRisk object
        ir = iriusrisk.IriusRisk('example.com', 'abc-123')

        # When check_response, then exception is raised
        with pytest.raises(iriusrisk.IriusCommonApiError):
            ir.check_response(response)

    @patch('startleft.iriusrisk.requests.get')
    def test_product_exists_invalid_notjson_response(self, mock_query):
        # Given a mocked bad response
        mock_query.return_value.ok = True
        mock_query.return_value.json = Mock(side_effect=JSONDecodeError('', '', 0))

        # And an IriusRisk object
        ir = iriusrisk.IriusRisk('example.com', 'abc-123')

        # And a mock to check_response method
        ir.check_response = MagicMock()

        # when product_exists()
        with pytest.raises(iriusrisk.IriusCommonApiError):
            ir.product_exists()

        assert ir.check_response.called

    @patch('startleft.iriusrisk.requests.get')
    def test_product_exists_valid_matching_response(self, mock_query):
        # Given a mocked good response
        mock_query.return_value.ok = True
        mock_query.return_value.json.return_value = [{"ref": "matchingid"}]

        # And an IriusRisk object
        ir = iriusrisk.IriusRisk('example.com', 'abc-123')

        # And a mock to check_response method
        ir.check_response = MagicMock()

        # when product_exists()
        # Then exception is raised
        ir.id = "matchingid"
        assert ir.product_exists()
        assert ir.check_response.called

    @patch('startleft.iriusrisk.requests.get')
    def test_product_exists_valid_nonmatching_response(self, mock_query):
        # Given a mocked good response
        mock_query.return_value.ok = True
        mock_query.return_value.json.return_value = [{"ref": "nonmatchingid"}]

        # And an IriusRisk object with a different project ref
        ir = iriusrisk.IriusRisk('example.com', 'abc-123')
        ir.id = "matchingid"

        # And a mock to check_response method
        ir.check_response = MagicMock()

        # Then product_exists will return false
        assert not ir.product_exists()
        assert ir.check_response.called
