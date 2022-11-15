import pytest

from slp_base import LoadingMappingFileError
from slp_mtmt.slp_mtmt.mtmt_mapping_file_loader import MTMTMappingFileLoader
from slp_mtmt.tests.resources import test_resource_paths
from slp_mtmt.tests.resources.test_resource_paths import custom_mtmt_single_mapping_file, \
    custom_mtmt_multiple_mapping_file, \
    no_mandatory_label_added_mtmt_mapping_file, trustzones_no_mandatory_label_added_mtmt_mapping_file, \
    default_mtmt_single_mapping_file, default_mtmt_multiple_mapping_file, custom_bad_formed_file, \
    default_mtmt_empty_elements


def get_mtmt_mapping(filename):
    mapping_data_list = []
    default_mapping_file = filename
    with open(default_mapping_file) as f:
        mapping_data_list.append(f.read())

    mtmt_mapping_file_loader = MTMTMappingFileLoader(mapping_data_list)
    mtmt_mapping_file_loader.load()

    return mtmt_mapping_file_loader.get_mtmt_mapping()


class TestMTMTMappingFileLoader:

    def test_mtmt_mapping_loader_load_single_elements_ok(self):
        # GIVEN a mapping file with a trustzone
        # AND a single component
        default_mapping_file = default_mtmt_single_mapping_file

        with open(default_mapping_file) as file:
            mapping_file_data = file.read()

        # WHEN the load method of the MtmtMappingFileLoader is called
        mtmt_mapping_file_loader = MTMTMappingFileLoader([mapping_file_data])
        mtmt_mapping_file_loader.load()

        # THEN a MtmtMapping is returned with a trustzone, a component and without dataflows
        mtmt_mapping = mtmt_mapping_file_loader.get_mtmt_mapping()
        assert len(mtmt_mapping.mapping_trustzones) == 1
        assert len(mtmt_mapping.mapping_components) == 1
        assert len(mtmt_mapping.mapping_dataflows) == 0
        assert mtmt_mapping.mapping_trustzones.get('Public Cloud').get('id') == 'b61d6911-338d-46a8-9f39-8dcd24abfe91'
        assert mtmt_mapping.mapping_components.get('Custom VPC').get('type') == 'empty-component'

    def test_mtmt_mapping_loader_with_empty_elements_ok(self):
        # GIVEN a mapping file without trustzones, without components and without dataflows
        default_mapping_file = default_mtmt_empty_elements

        with open(default_mapping_file) as file:
            mapping_file_data = file.read()

        # WHEN the load method of the MtmtMappingFileLoader is called
        mtmt_mapping_file_loader = MTMTMappingFileLoader([mapping_file_data])
        mtmt_mapping_file_loader.load()

        # THEN a MtmtMapping is returned without trustzones, components or dataflows
        mtmt_mapping = mtmt_mapping_file_loader.get_mtmt_mapping()
        assert len(mtmt_mapping.mapping_trustzones) == 0
        assert len(mtmt_mapping.mapping_components) == 0
        assert len(mtmt_mapping.mapping_dataflows) == 0

    def test_mtmt_mapping_loader_load_multiple_elements_ok(self):
        # GIVEN a mapping file with many trustzones
        # AND many components
        default_mapping_file = default_mtmt_multiple_mapping_file

        with open(default_mapping_file) as file:
            mapping_file_data = file.read()

        # WHEN the load method of the MtmtMappingFileLoader is called
        mtmt_mapping_file_loader = MTMTMappingFileLoader([mapping_file_data])
        mtmt_mapping_file_loader.load()

        # THEN a MtmtMapping is returned with many trustzones, many components and without dataflows
        mtmt_mapping = mtmt_mapping_file_loader.get_mtmt_mapping()
        assert len(mtmt_mapping.mapping_trustzones) == 2
        assert len(mtmt_mapping.mapping_components) == 3
        assert len(mtmt_mapping.mapping_dataflows) == 0
        assert mtmt_mapping.mapping_trustzones.get('Internet').get('id') == 'f0ba7722-39b6-4c81-8290-a30a248bb8d9'
        assert mtmt_mapping.mapping_components.get('Custom enterprise GW').get('label') == 'Custom enterprise GW'

    @pytest.mark.parametrize('mapping_file',
                             [no_mandatory_label_added_mtmt_mapping_file,
                              trustzones_no_mandatory_label_added_mtmt_mapping_file])
    def test_mtmt_mapping_loader_with_not_mandatory_labels_ok(self, mapping_file: str):
        # GIVEN a mapping file with some additional label
        default_mapping_file = mapping_file

        with open(default_mapping_file) as file:
            mapping_file_data = file.read()

        # WHEN the load method of the MtmtMappingFileLoader is called
        mtmt_mapping_file_loader = MTMTMappingFileLoader([mapping_file_data])
        mtmt_mapping_file_loader.load()

        # THEN a MtmtMapping is returned with a trustzone, a component and without dataflows
        # AND the additional label is empty
        mtmt_mapping = mtmt_mapping_file_loader.get_mtmt_mapping()
        assert len(mtmt_mapping.mapping_trustzones) == 1
        assert len(mtmt_mapping.mapping_components) == 1
        assert len(mtmt_mapping.mapping_dataflows) == 0
        assert len(mtmt_mapping.mapping_trustzones.get('Public Cloud')) == 4
        assert mtmt_mapping.mapping_trustzones.get('Public Cloud').get('dummy') == ''

    def test_mtmt_mapping_loader_with_default_and_custom_mapping_files_ok(self):
        # GIVEN a default mapping file with a trustzone
        # AND a single component
        mapping_data_list = []
        default_mapping_file = default_mtmt_single_mapping_file
        with open(default_mapping_file) as f:
            mapping_data_list.append(f.read())

        # AND a custom mapping file with a trustzone
        # AND a single component
        custom_mapping_file = custom_mtmt_single_mapping_file
        with open(custom_mapping_file) as f:
            mapping_data_list.append(f.read())

        # WHEN the load method of the MtmtMappingFileLoader is called
        mtmt_mapping_file_loader = MTMTMappingFileLoader(mapping_data_list)
        mtmt_mapping_file_loader.load()

        # THEN a MtmtMapping is returned with a trustzone, a component and without dataflows
        mtmt_mapping = mtmt_mapping_file_loader.get_mtmt_mapping()
        assert len(mtmt_mapping.mapping_trustzones) == 2
        assert len(mtmt_mapping.mapping_components) == 2
        assert len(mtmt_mapping.mapping_dataflows) == 0
        assert mtmt_mapping.mapping_trustzones.get('Public Cloud').get(
            'id') == 'b61d6911-338d-46a8-9f39-8dcd24abfe91'
        assert mtmt_mapping.mapping_trustzones.get('Private Cloud').get(
            'id') == 'b5485-430d-52d5-6h40-8gdfg205'
        assert mtmt_mapping.mapping_components.get('Custom VPC').get('type') == 'empty-component'
        assert mtmt_mapping.mapping_components.get('Custom enterprise GW').get('type') == 'empty-component'

    def test_mtmt_mapping_loader_with_default_and_custom_mapping_files_with_multiple_items_ok(self):
        # GIVEN a default mapping file with a trustzone
        # AND two components
        mapping_data_list = []
        default_mapping_file = default_mtmt_multiple_mapping_file
        with open(default_mapping_file) as f:
            mapping_data_list.append(f.read())

        # AND a custom mapping file with 2 trustzones
        # AND 3 components
        custom_mapping_file = custom_mtmt_multiple_mapping_file
        with open(custom_mapping_file) as f:
            mapping_data_list.append(f.read())

        # WHEN the load method of the MtmtMappingFileLoader is called
        mtmt_mapping_file_loader = MTMTMappingFileLoader(mapping_data_list)
        mtmt_mapping_file_loader.load()

        # THEN a MtmtMapping is returned with 3 trustzones, 5 components and without dataflows
        mtmt_mapping = mtmt_mapping_file_loader.get_mtmt_mapping()
        assert len(mtmt_mapping.mapping_trustzones) == 3
        assert len(mtmt_mapping.mapping_components) == 5
        assert len(mtmt_mapping.mapping_dataflows) == 0
        assert mtmt_mapping.mapping_trustzones.get('Public Cloud').get(
            'id') == 'b61d6911-338d-46a8-9f39-8dcd24abfe91'
        assert mtmt_mapping.mapping_trustzones.get('Private Secured Cloud').get(
            'id') == '2ab4effa-40b7-4cd2-ba81-8247d29a6f2d'
        assert mtmt_mapping.mapping_components.get('Custom web server').get('type') == 'empty-component'
        assert mtmt_mapping.mapping_components.get('Custom enterprise GW Test').get('type') == 'empty-component'

    @pytest.mark.parametrize('default_mapping_file,custom_mapping_file',
                             [(default_mtmt_multiple_mapping_file, custom_bad_formed_file),
                              (custom_bad_formed_file, custom_mtmt_single_mapping_file)])
    def test_mtmt_mapping_loader_validation_error(self, default_mapping_file: str, custom_mapping_file: str):
        # GIVEN a valid default mapping file
        mapping_data_list = []
        with open(default_mapping_file) as f:
            mapping_data_list.append(f.read())

        # AND a custom mapping file with invalid format
        with open(custom_mapping_file) as f:
            mapping_data_list.append(f.read())

        # WHEN the load method of the MtmtMappingFileLoader is called
        mtmt_mapping_file_loader = MTMTMappingFileLoader(mapping_data_list)

        # THEN an error LoadingMappingFileError is raised
        with pytest.raises(LoadingMappingFileError) as e_info:
            mtmt_mapping_file_loader.load()
        assert e_info.value.error_code.http_status == 400
        assert e_info.value.error_code.name == 'MAPPING_LOADING_ERROR'

    def test_mtmt_mapping_loader_with_several_types(self):
        # WHEN we load the mapping file with types
        mtmt_mapping = get_mtmt_mapping(test_resource_paths.mtmt_default_mapping)

        # THEN we check the components and trustzones are correctly mapped
        assert len(mtmt_mapping.mapping_trustzones) == 6
        assert len(mtmt_mapping.mapping_components) == 57
        assert len(mtmt_mapping.mapping_dataflows) == 0
        assert mtmt_mapping.mapping_trustzones.get('Internet Boundary').get(
            'id') == 'f0ba7722-39b6-4c81-8290-a30a248bb8d9'
        assert mtmt_mapping.mapping_trustzones.get('CorpNet Trust Boundary').get(
            'id') == '2ab4effa-40b7-4cd2-ba81-8247d29a6f2d'
        assert mtmt_mapping.mapping_trustzones.get('Generic Trust Border Boundary').get(
            'id') == '6376d53e-6461-412b-8e04-7b3fe2b397de'
        assert mtmt_mapping.mapping_trustzones.get('Generic Trust Line Boundary').get(
            'id') == '6376d53e-6461-412b-8e04-7b3fe2b397de'
        assert mtmt_mapping.mapping_trustzones.get('Sandbox Trust Boundary Border').get(
            'id') == '2ab4effa-40b7-4cd2-ba81-8247d29a6f2d'
        assert mtmt_mapping.mapping_trustzones.get('default').get('id') == 'b61d6911-338d-46a8-9f39-8dcd24abfe91'
        assert mtmt_mapping.mapping_components.get('ADFS').get('type') == 'active-directory'
        mobile_client = mtmt_mapping.mapping_components.get('Mobile Client')
        assert mobile_client['key'] == 'Mobile Client Technologies'
        values = mobile_client['values']
        assert values[0]['value'] == 'Android'
        assert values[0]['type'] == 'android-device-client'
        assert values[1]['value'] == 'iOS'
        assert values[1]['type'] == 'ios-device-client'
