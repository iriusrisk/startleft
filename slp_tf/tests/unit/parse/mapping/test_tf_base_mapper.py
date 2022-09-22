from unittest.mock import patch, MagicMock

from slp_tf.slp_tf.parse.mapping.mappers.tf_base_mapper import TerraformBaseMapper


class TestTerraformBaseMapper:

    @patch("slp_tf.slp_tf.parse.mapping.tf_sourcemodel.TerraformSourceModel")
    def test_get_tags_with_mapping_str(self, mock_source_model):
        mock_source_model.search.return_value = 'value'
        c_tags = TerraformBaseMapper.get_tags(mock_source_model, MagicMock(), MagicMock())
        assert len(c_tags) is 1

    @patch("slp_tf.slp_tf.parse.mapping.tf_sourcemodel.TerraformSourceModel")
    def test_get_tags_with_mapping_list(self, mock_source_model):
        mock_source_model.search.return_value = 'value'
        c_tags = TerraformBaseMapper.get_tags(mock_source_model, MagicMock(), [MagicMock(), MagicMock()])
        assert len(c_tags) is 2

    @patch("slp_tf.slp_tf.parse.mapping.tf_sourcemodel.TerraformSourceModel")
    def test_get_tags_with_attribute_not_found(self, mock_source_model):
        mock_source_model.search.return_value = []
        c_tags = TerraformBaseMapper.get_tags(mock_source_model, MagicMock(), MagicMock())
        assert len(c_tags) is 0
