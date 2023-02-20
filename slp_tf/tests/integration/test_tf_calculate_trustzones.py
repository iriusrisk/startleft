from sl_util.sl_util.file_utils import get_data
from slp_tf.tests.resources import test_resource_paths
from slp_tf import TerraformProcessor
from slp_base.tests.util.otm import validate_and_compare

SAMPLE_ID = 'id'
SAMPLE_NAME = 'name'


class TestTerraformCalculateTrustzones:

    def test_trustzone_types(self):
        # GIVEN a valid TF file
        terraform_file = get_data(test_resource_paths.terraform_minimal_content)

        # AND a valid TF mapping file that defines two TZs, one with type and the one without type
        mapping_file = get_data(test_resource_paths.terraform_trustzone_types_mapping)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN an empty OTM containing only the default trustzone is generated
        result, expected = validate_and_compare(otm.json(), test_resource_paths.terraform_minimal_content_otm, None)
        assert result == expected

    def test_components_with_trustzones_of_same_type(self):
        # GIVEN a valid TF file WITH some components mapped to different TZs of the same type
        terraform_file = get_data(test_resource_paths.terraform_components_with_trustzones_of_same_type)

        # AND a valid TF mapping file that defines two different TZs of the same type
        mapping_file = get_data(test_resource_paths.terraform_multiple_trustzones_same_type_mapping)

        # WHEN the TF file is processed
        otm = TerraformProcessor(SAMPLE_ID, SAMPLE_NAME, [terraform_file], [mapping_file]).process()

        # THEN an empty OTM containing only the default trustzone is generated
        result, expected = validate_and_compare(otm.json(),
                                                test_resource_paths.tf_components_with_trustzones_of_same_type_otm,
                                                None)
        assert result == expected
