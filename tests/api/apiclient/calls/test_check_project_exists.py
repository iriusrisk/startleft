from json import JSONDecodeError
from unittest.mock import Mock, patch, MagicMock

import pytest

from startleft.api.errors import IriusCommonApiError
from startleft.apiclient.calls.check_project_exists import CheckProjectExists


class TestBaseApiClient:

    @patch('startleft.apiclient.base_api_client.requests.get')
    def test_project_exists_invalid_not_json_response(self, mock_query):
        # Given a mocked bad response
        mock_query.return_value.ok = True
        mock_query.return_value.json = Mock(side_effect=JSONDecodeError('', '', 0))

        # And an IriusRisk object
        check_project_exists = CheckProjectExists('example.com', 'abc-123')

        # when project_exists()
        # Then
        with pytest.raises(IriusCommonApiError):
            check_project_exists.do_call(project_id='1')

        assert mock_query.call_count == 1

    @patch('startleft.apiclient.base_api_client.requests.get')
    def test_project_exists_valid_matching_response(self, mock_query):
        # Given a mocked good response
        mock_query.return_value.ok = True
        mock_query.return_value.json.return_value = [{"ref": "matchingid"}]

        # And an IriusRisk object
        check_project_exists = CheckProjectExists('example.com', 'abc-123')

        # when project_exists()

        # Then
        assert check_project_exists.do_call(project_id="matchingid")
        assert mock_query.call_count == 1

    @patch('startleft.apiclient.base_api_client.requests.get')
    def test_project_exists_valid_nonmatching_response(self, mock_query):
        # Given a mocked good response
        mock_query.return_value.ok = True
        mock_query.return_value.json.return_value = [{"ref": "nonmatchingid"}]

        # And an IriusRisk object with a different project ref
        check_project_exists = CheckProjectExists('example.com', 'abc-123')

        # Then project_exists will return false
        assert not check_project_exists.do_call(project_id="matchingid")
        assert mock_query.call_count == 1
