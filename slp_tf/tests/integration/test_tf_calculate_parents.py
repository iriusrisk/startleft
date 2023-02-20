import pytest

from sl_util.sl_util.file_utils import get_data
from slp_base import OTMBuildingError
from slp_base.tests.util.otm import validate_and_compare
from slp_tf import TerraformProcessor
from slp_tf.tests.resources import test_resource_paths
from slp_tf.tests.resources.test_resource_paths import expected_orphan_component_is_not_mapped, \
    expected_mapping_skipped_component_without_parent, tf_mapping_parent_by_full_path_attribute, \
    tf_mapping_parent_by_type_name, tf_mapping_parent_by_name
from slp_tf.tests.resources.test_resource_paths import terraform_iriusrisk_tf_aws_mapping
from slp_tf.tests.utility import excluded_regex

SAMPLE_ID = 'id'
SAMPLE_NAME = 'name'


class TestTerraformCalculateParents:

    @pytest.mark.parametrize('mapping_file', [terraform_iriusrisk_tf_aws_mapping])
    def test_orphan_component_is_not_mapped(self, mapping_file):
        # GIVEN a valid TF file with a resource (VPCssm) whose parents do (private VPCs) not exist in the file
        terraform_file = get_data(test_resource_paths.terraform_orphan_component)

        # AND a valid TF mapping file
        mapping_file = get_data(mapping_file)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN the VPCsmm components without parents are omitted
        # AND the rest of the OTM details match the expected
        result, expected = validate_and_compare(otm.json(), expected_orphan_component_is_not_mapped, excluded_regex)
        assert result == expected

    def test_mapping_component_without_parent(self):
        # GIVEN a valid TF file
        terraform_file = get_data(test_resource_paths.terraform_component_without_parent)

        # AND an invalid TF mapping file with a mapping without parent
        mapping_file = get_data(test_resource_paths.terraform_mapping_aws_component_without_parent)

        # WHEN the TF file is processed
        # THEN an OTMBuildingError is raised
        with pytest.raises(OTMBuildingError) as e_info:
            TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # AND the error references a parent issue
        assert 'KeyError' == e_info.value.detail
        assert "'parent'" == e_info.value.message

    def test_mapping_skipped_component_without_parent(self):
        # GIVEN a valid TF file
        terraform_file = get_data(test_resource_paths.terraform_skipped_component_without_parent)

        # AND a TF mapping file that skips the component without parent
        mapping_file = get_data(test_resource_paths.terraform_mapping_aws_component_without_parent)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN the resulting OTM match the expected one
        result, expected = validate_and_compare(otm, expected_mapping_skipped_component_without_parent,
                                 excluded_regex)
        assert result == expected

    @pytest.mark.parametrize('mapping_file', [
        pytest.param(get_data(tf_mapping_parent_by_type_name), id="by {type}.{name}"),
        pytest.param(get_data(tf_mapping_parent_by_full_path_attribute), id="by full path attribute"),
        pytest.param(get_data(tf_mapping_parent_by_name), id="by {name}")])
    def test_define_parent_relationship(self, mapping_file):
        """
        Generate an OTM for TF file with parent definition
        """
        # GIVEN a TF file with two resources
        #    AND a mapping file with parent definition
        tf_file = get_data(test_resource_paths.terraform_define_parent_relationship)

        # WHEN processing
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [tf_file], [mapping_file]).process()

        # THEN a valid OTM is returned without errors
        #    AND resource_be defines resource_a as parent
        assert len(otm.components) == 2
        assert otm.components[0].name == "resource_a"
        assert otm.components[1].name == "resource_b"
        assert otm.components[1].parent == otm.components[0].id
