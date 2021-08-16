from unittest import mock
from unittest.mock import Mock, patch
from json import JSONDecodeError
import pytest
from startleft import iriusrisk

class TestIriusRisk:

    @patch('startleft.iriusrisk.requests.get')
    def test_product_exists_invalid_response(self, mock_query):
        mock_query.return_value.ok = False
        ir = iriusrisk.IriusRisk('example.com', 'abc-123')        
        with pytest.raises(iriusrisk.IriusApiError):
            ir.product_exists()

    @patch('startleft.iriusrisk.requests.get')
    def test_product_exists_invalid_notjson_response(self, mock_query):
        mock_query.return_value.ok = True
        mock_query.return_value.json = Mock(side_effect=JSONDecodeError('', '', 0))
        ir = iriusrisk.IriusRisk('example.com', 'abc-123')
        with pytest.raises(iriusrisk.IriusApiError):
            ir.product_exists()

    @patch('startleft.iriusrisk.requests.get')
    def test_product_exists_valid_matching_response(self, mock_query):
        mock_query.return_value.ok = True
        mock_query.return_value.json.return_value = [{"ref":"matchingid"}]
        ir = iriusrisk.IriusRisk('example.com', 'abc-123')
        ir.id = "matchingid"        
        assert ir.product_exists() == True

    @patch('startleft.iriusrisk.requests.get')
    def test_product_exists_valid_nonmatching_response(self, mock_query):
        mock_query.return_value.ok = True
        mock_query.return_value.json.return_value = [{"ref":"nonmatchingid"}]
        ir = iriusrisk.IriusRisk('example.com', 'abc-123')
        ir.id = "matchingid"        
        assert ir.product_exists() == False