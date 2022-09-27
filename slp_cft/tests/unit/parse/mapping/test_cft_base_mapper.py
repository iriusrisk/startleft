from unittest.mock import patch, MagicMock

from slp_cft.slp_cft.parse.mapping.mappers.cft_base_mapper import CloudformationBaseMapper


class TestCloudformationBaseMapper:

    @patch("slp_cft.slp_cft.parse.mapping.cft_sourcemodel.CloudformationSourceModel")
    def test_get_tags_with_mapping_str(self, mock_source_model):
        mock_source_model.search.return_value = 'value'
        c_tags = CloudformationBaseMapper.get_tags(mock_source_model, MagicMock(), MagicMock())
        assert len(c_tags) is 1

    @patch("slp_cft.slp_cft.parse.mapping.cft_sourcemodel.CloudformationSourceModel")
    def test_get_tags_with_mapping_list(self, mock_source_model):
        mock_source_model.search.return_value = 'value'
        c_tags = CloudformationBaseMapper.get_tags(mock_source_model, MagicMock(), [MagicMock(), MagicMock()])
        assert len(c_tags) is 2

    @patch("slp_cft.slp_cft.parse.mapping.cft_sourcemodel.CloudformationSourceModel")
    def test_get_tags_with_attribute_not_found(self, mock_source_model):
        mock_source_model.search.return_value = []
        c_tags = CloudformationBaseMapper.get_tags(mock_source_model, MagicMock(), MagicMock())
        assert len(c_tags) is 0
