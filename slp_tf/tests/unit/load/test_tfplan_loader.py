from copy import deepcopy
from json import JSONDecodeError
from unittest.mock import patch

from pytest import mark, param, raises

from sl_util.sl_util.file_utils import get_data
from slp_tf.tests.resources import test_resource_paths
from slp_base import LoadingIacFileError
from slp_tf.slp_tf.load.tfplan_loader import is_tfplan, TfplanLoader

INVALID_YAML = test_resource_paths.invalid_yaml
TFPLAN_MINIMUM_STRUCTURE = {'planned_values': {'root_module': {}}}
TF_FILE_YAML_EXCEPTION = JSONDecodeError('HLC2 cannot be processed as JSON', doc='sample-doc', pos=0)


def build_tfplan(resources: [{}] = None, child_modules: [{}] = None) -> {}:
    tfplan = deepcopy(TFPLAN_MINIMUM_STRUCTURE)

    if resources:
        tfplan['planned_values']['root_module']['resources'] = resources

    if child_modules:
        tfplan['planned_values']['root_module']['child_modules'] = child_modules

    return tfplan


def generate_resources(resource_count: int, module_child: bool = False) -> [{}]:
    resources = []
    for i in range(1, resource_count + 1):
        resource = {
            'address': f'r{i}-addr',
            'mode': 'managed',
            'type': f'r{i}-type',
            'name': f'r{i}-name',
            'provider_name': 'registry.terraform.io/hashicorp/aws',
            'schema_version': 0,
            'values': {
                'val1': 'value1',
                'val2': 'value2',
            },
            'sensitive_values': {
                'senval1': 'value1',
                'senval2': 'value2',
            }
        }

        if module_child:
            resource['index'] = 0

        resources.append(resource)

    return resources


def generate_child_modules(module_count: int, child_modules: [{}] = None, resource_count: int = None) -> [{}]:
    modules = []
    for i in range(1, module_count + 1):
        module = {
            'address': f'cm{i}-addr',
        }

        if child_modules:
            module['child_modules'] = child_modules

        if resource_count:
            module['resources'] = generate_resources(resource_count, True)

        modules.append(module)

    return modules


def assert_common_properties(properties: {}):
    assert properties['resource_mode'] == 'managed'
    assert properties['resource_provider_name'] == 'registry.terraform.io/hashicorp/aws'
    assert properties['resource_schema_version'] == 0
    assert properties['val1'] == 'value1'
    assert properties['senval1'] == 'value1'


def assert_resource_id(resource: {}):
    assert resource['resource_id'] == f'{resource["resource_type"]}.{resource["resource_name"]}'


def assert_retro_compatibility_fields(resource: {}):
    assert list(resource.keys())[0] == resource['resource_type']
    assert resource['Type'] == resource['resource_type']
    assert resource['_key'] == resource['resource_name']
    assert resource['Properties'] == resource['resource_properties']
    assert resource[resource['resource_type']][resource['resource_name']] == resource['resource_properties']


class TestTfplanLoader:

    @mark.parametrize('yaml_side_effect,expected', [
        param(TFPLAN_MINIMUM_STRUCTURE, True, id='TFPLAN'),
        param(TF_FILE_YAML_EXCEPTION, False, id='TF')
    ])
    def test_is_tf_plan_single_file(self, yaml_side_effect, expected: bool):
        # GIVEN a single valid terraform source file (TF or TFPLAN)
        # WHEN TfplanLoader::is_tfplan is invoked
        # THEN return true if the source is a TFPLAN or false otherwise
        with patch('json.loads', side_effect=[yaml_side_effect]):
            assert is_tfplan(sources=['MOCKED']) == expected

    @patch('json.loads')
    def test_is_tf_plan_multiple_tf_files(self, yaml_mock):
        # GIVEN multiple valid TF source files
        yaml_mock.side_effect = [TF_FILE_YAML_EXCEPTION, TF_FILE_YAML_EXCEPTION]

        # WHEN TfplanLoader::is_tfplan is invoked
        # THEN return false
        assert not is_tfplan(sources=['MOCKED', 'MOCKED'])

    @patch('json.loads')
    def test_is_tf_plan_multiple_tfplan_files(self, yaml_mock):
        # GIVEN multiple valid TFPLAN source files
        yaml_mock.side_effect = [TFPLAN_MINIMUM_STRUCTURE, TFPLAN_MINIMUM_STRUCTURE]

        # WHEN TfplanLoader::is_tfplan is invoked
        # THEN a LoadingIacFileError exception is raised
        with raises(LoadingIacFileError) as loading_error:
            is_tfplan(sources=['MOCKED', 'MOCKED'])

        # AND the message says that no multiple tfplan files can be processed at the same time
        assert str(loading_error.value.title) == 'Multiple Terraform plan files'
        assert str(loading_error.value.message) == 'Multiple Terraform plan files cannot be loaded at the same time.'

    @patch('json.loads')
    def test_is_tf_plan_multiple_files_mixed(self, yaml_mock):
        # GIVEN multiple valid TFPLAN and TF source files
        yaml_mock.side_effect = [TF_FILE_YAML_EXCEPTION, TFPLAN_MINIMUM_STRUCTURE]

        # WHEN TfplanLoader::is_tfplan is invoked
        # THEN a LoadingIacFileError exception is raised
        with raises(LoadingIacFileError) as error:
            is_tfplan(sources=['MOCKED', 'MOCKED'])

        # AND the message says that TF and TFPLAN files cannot be loaded at the same time
        assert str(error.value.title) == 'Mixed Terraform files'
        assert str(error.value.message) == 'Terraform Config and Plan files cannot be loaded at the same time.'

    @patch('yaml.load')
    def test_load_no_modules(self, yaml_mock):
        # GIVEN a valid plain Terraform Plan file with no modules
        yaml_mock.side_effect = [build_tfplan(resources=generate_resources(2))]

        # WHEN TfplanLoader::load is invoked
        tfplan_loader = TfplanLoader(source='MOCKED')
        tfplan_loader.load()

        # THEN TF contents are loaded in TfplanLoader.terraform
        assert tfplan_loader.terraform
        resources = tfplan_loader.terraform['resource']
        assert len(resources) == 2

        # AND resource_id, resource_type, resource_name and resource_properties are right

        for i, resource in enumerate(resources):
            i += 1
            assert_resource_id(resource)
            assert resource['resource_type'] == f'r{i}-type'
            assert resource['resource_name'] == f'r{i}-name'

            properties = resource['resource_properties']
            assert_common_properties(properties)
            assert_retro_compatibility_fields(resource)
            assert properties['resource_address'] == f'r{i}-addr'

    @patch('yaml.load')
    def test_load_only_modules(self, yaml_mock):
        # GIVEN a valid plain Terraform Plan file with only modules
        yaml_mock.side_effect = [build_tfplan(
            child_modules=generate_child_modules(module_count=2, resource_count=2))]

        # WHEN TfplanLoader::load is invoked
        tfplan_loader = TfplanLoader(source='MOCKED')
        tfplan_loader.load()

        # THEN TF contents are loaded in TfplanLoader.terraform
        assert tfplan_loader.terraform
        resources = tfplan_loader.terraform['resource']
        assert len(resources) == 4

        # AND resource_id, resource_type, resource_name and resource_properties are right
        resource_index = 0
        for module_index in range(1, 3):
            module_address = f'cm{module_index}-addr'

            for child_index in range(1, 3):
                resource = resources[resource_index]

                assert_resource_id(resource)
                assert resource['resource_type'] == f'r{child_index}-type'
                assert resource['resource_name'] == f'{module_address}.r{child_index}-name_0'

                properties = resource['resource_properties']
                assert properties['resource_address'] == f'r{child_index}-addr'
                assert_common_properties(properties)
                assert_retro_compatibility_fields(resource)

                resource_index += 1

    @patch('yaml.load')
    def test_load_nested_modules(self, yaml_mock):
        # GIVEN a valid plain Terraform Plan file with nested modules
        yaml_mock.side_effect = [build_tfplan(
            child_modules=generate_child_modules(
                module_count=1,
                child_modules=generate_child_modules(module_count=1, resource_count=1)))]

        # WHEN TfplanLoader::load is invoked
        tfplan_loader = TfplanLoader(source='MOCKED')
        tfplan_loader.load()

        # THEN TF contents are loaded in TfplanLoader.terraform
        assert tfplan_loader.terraform
        resources = tfplan_loader.terraform['resource']
        resource = resources[0]

        # AND resource_id, resource_type, resource_name and resource_properties are right
        assert len(resources) == 1

        assert_resource_id(resource)
        assert resource['resource_type'] == 'r1-type'
        assert resource['resource_name'] == 'cm1-addr.cm1-addr.r1-name_0'

        properties = resource['resource_properties']
        assert properties['resource_address'] == 'r1-addr'
        assert_common_properties(properties)
        assert_retro_compatibility_fields(resource)

    @patch('yaml.load')
    def test_load_complex_structure(self, yaml_mock):
        # GIVEN a valid plain Terraform Plan file with modules and root-level resources
        yaml_mock.side_effect = [build_tfplan(
            resources=generate_resources(1),
            child_modules=generate_child_modules(module_count=1, resource_count=1))]

        # WHEN TfplanLoader::load is invoked
        tfplan_loader = TfplanLoader(source='MOCKED')
        tfplan_loader.load()

        # THEN TF contents are loaded in TfplanLoader.terraform
        assert tfplan_loader.terraform
        resources = tfplan_loader.terraform['resource']
        assert len(resources) == 2

        # AND resource_type, resource_name and resource_properties from top level are right
        resource = resources[0]

        assert_resource_id(resource)
        assert resource['resource_type'] == 'r1-type'
        assert resource['resource_name'] == 'r1-name'

        properties = resource['resource_properties']
        assert properties['resource_address'] == 'r1-addr'
        assert_common_properties(properties)
        assert_retro_compatibility_fields(resource)

        # AND resource_type, resource_name and resource_properties from child modules are right
        resource = resources[1]
        assert_resource_id(resource)
        assert resource['resource_type'] == 'r1-type'
        assert resource['resource_name'] == 'cm1-addr.r1-name_0'

        properties = resource['resource_properties']
        assert properties['resource_address'] == 'r1-addr'
        assert_common_properties(properties)
        assert_retro_compatibility_fields(resource)

    @patch('yaml.load')
    def test_load_resources_same_name(self, yaml_mock):
        # GIVEN a valid plain Terraform Plan file with only one module
        tfplan = build_tfplan(
            child_modules=generate_child_modules(module_count=1, resource_count=1))

        # AND two resources with the same name
        tfplan_resources = tfplan['planned_values']['root_module']['child_modules'][0]['resources']
        duplicated_resource = deepcopy(tfplan_resources[0])
        duplicated_resource['index'] = 1
        tfplan_resources.append(duplicated_resource)

        yaml_mock.side_effect = [tfplan]

        # WHEN TfplanLoader::load is invoked
        tfplan_loader = TfplanLoader(source='MOCKED')
        tfplan_loader.load()

        # THEN TF contents are loaded in TfplanLoader.terraform
        assert tfplan_loader.terraform
        resources = tfplan_loader.terraform['resource']
        assert len(resources) == 2

        # AND The name and resource ids are differentiated by the index suffix
        assert resources[0]['resource_id'] == 'r1-type.cm1-addr.r1-name_0'
        assert resources[0]['resource_name'] == 'cm1-addr.r1-name_0'

        assert resources[1]['resource_id'] == 'r1-type.cm1-addr.r1-name_1'
        assert resources[1]['resource_name'] == 'cm1-addr.r1-name_1'

    @patch('yaml.load')
    def test_load_no_resources(self, yaml_mock):
        # GIVEN a valid Terraform Plan file with no resources
        yaml_mock.side_effect = [{'planned_values': {'root_module': {}}}]

        # WHEN TfplanLoader::load is invoked
        tfplan_loader = TfplanLoader(source='MOCKED')
        tfplan_loader.load()

        # THEN TfplanLoader.terraform is an empty dictionary
        assert tfplan_loader.terraform == {}

    @patch('yaml.load')
    def test_load_empty_tfplan(self, yaml_mock):
        # GIVEN an empty TFPLAN
        yaml_mock.side_effect = [{}]

        # WHEN TfplanLoader::load is invoked
        tfplan_loader = TfplanLoader(source='MOCKED')
        tfplan_loader.load()

        # THEN TfplanLoader.terraform is an empty dictionary
        assert tfplan_loader.terraform == {}

    def test_load_invalid_wrong_json(self):
        # GIVEN an invalid Terraform source file (TF or TFPLAN)
        sources = get_data(INVALID_YAML)

        # WHEN TfplanLoader::load is invoked
        # THEN a LoadingIacFileError is raised
        with raises(LoadingIacFileError) as loading_error:
            TfplanLoader(sources).load()

        # AND an empty IaC file message is on the exception
        assert str(loading_error.value.title) == 'IaC file is not valid'
        assert str(loading_error.value.message) == 'The provided IaC file could not be processed'
