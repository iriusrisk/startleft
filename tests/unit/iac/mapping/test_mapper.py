from unittest.mock import patch, MagicMock

from startleft.iac.mapping.mapper import get_tags


class TestMapper:

    @patch("startleft.iac.mapping.sourcemodel.SourceModel")
    def test_get_tags_with_mapping_str(self, mock_source_model):
        mock_source_model.search.return_value = 'value'
        c_tags = get_tags(mock_source_model, MagicMock(), MagicMock())
        assert len(c_tags) is 1

    @patch("startleft.iac.mapping.sourcemodel.SourceModel")
    def test_get_tags_with_mapping_list(self, mock_source_model):
        mock_source_model.search.return_value = 'value'
        c_tags = get_tags(mock_source_model, MagicMock(), [MagicMock(), MagicMock()])
        assert len(c_tags) is 2

    @patch("startleft.iac.mapping.sourcemodel.SourceModel")
    def test_get_tags_with_attribute_not_found(self, mock_source_model):
        mock_source_model.search.return_value = []
        c_tags = get_tags(mock_source_model, MagicMock(), MagicMock())
        assert len(c_tags) is 0
