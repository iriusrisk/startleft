from copy import deepcopy
from json import JSONDecodeError
from unittest.mock import patch

from networkx import DiGraph
from pytest import raises

from slp_tf.slp_tf.tfplan.load.tfplan_loader import TfplanLoader
from sl_util.sl_util.file_utils import get_byte_data
from slp_tf.tests.resources import test_resource_paths
from slp_base import LoadingIacFileError

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
            resource['index'] = '0'

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
    assert resource['resource_id'] == resource['properties']['resource_address']


def assert_retro_compatibility_fields(resource: {}):
    assert list(resource.keys())[0] == resource['resource_type']
    assert resource['Type'] == resource['resource_type']
    assert resource['_key'] == resource['resource_name']
    assert resource['Properties'] == resource['resource_properties']
    assert resource[resource['resource_type']][resource['resource_name']] == resource['resource_properties']


class TestTfplanLoader:

    @patch('slp_tf.slp_tf.tfplan.load.tfplan_loader.load_tfgraph')
    @patch('yaml.load')
    def test_load_tfplan_and_graph(self, yaml_mock, from_agraph_mock):
        # GIVEN a valid plain Terraform Plan file with no modules
        yaml_mock.side_effect = [build_tfplan(resources=generate_resources(2))]

        # AND a mocked graph load result
        graph_label = 'Mocked Graph'
        from_agraph_mock.side_effect = [DiGraph(label=graph_label)]

        # WHEN TfplanLoader::load is invoked
        tfplan_loader = TfplanLoader(tfplan_source=b'MOCKED', tfgraph_source=b'MOCKED')
        tfplan_loader.load()

        # THEN the TFPLAN is loaded
        assert tfplan_loader.get_terraform() is not None

        # AND the TFGRAPH is also loaded
        assert tfplan_loader.get_tfgraph().graph['label'] == graph_label

    @patch('yaml.load')
    def test_load_no_modules(self, yaml_mock):
        # GIVEN a valid plain Terraform Plan file with no modules
        yaml_mock.side_effect = [build_tfplan(resources=generate_resources(2))]

        # WHEN TfplanLoader::load is invoked
        tfplan_loader = TfplanLoader(tfplan_source=b'MOCKED')
        tfplan_loader.load()

        # THEN TF contents are loaded in TfplanLoader.terraform
        assert tfplan_loader.terraform
        resources = tfplan_loader.terraform['resource']
        assert len(resources) == 2

        # AND resource_id, resource_type, resource_name and resource_properties are right

        for i, resource in enumerate(resources):
            i += 1
            assert resource['resource_id'] == f'r{i}-addr'
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
        tfplan_loader = TfplanLoader(tfplan_source=b'MOCKED')
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

                assert resource['resource_id'] == f'r{child_index}-addr'
                assert resource['resource_type'] == f'r{child_index}-type'
                assert resource['resource_name'] == f'{module_address}.r{child_index}-name'

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
        tfplan_loader = TfplanLoader(tfplan_source=b'MOCKED')
        tfplan_loader.load()

        # THEN TF contents are loaded in TfplanLoader.terraform
        assert tfplan_loader.terraform
        resources = tfplan_loader.terraform['resource']
        resource = resources[0]

        # AND resource_id, resource_type, resource_name and resource_properties are right
        assert len(resources) == 1

        assert resource['resource_id'] == 'r1-addr'
        assert resource['resource_type'] == 'r1-type'
        assert resource['resource_name'] == 'cm1-addr.cm1-addr.r1-name'

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
        tfplan_loader = TfplanLoader(tfplan_source=b'MOCKED')
        tfplan_loader.load()

        # THEN TF contents are loaded in TfplanLoader.terraform
        assert tfplan_loader.terraform
        resources = tfplan_loader.terraform['resource']
        assert len(resources) == 2

        # AND resource_type, resource_name and resource_properties from top level are right
        resource = resources[0]

        assert resource['resource_id'] == 'r1-addr'
        assert resource['resource_type'] == 'r1-type'
        assert resource['resource_name'] == 'r1-name'

        properties = resource['resource_properties']
        assert properties['resource_address'] == 'r1-addr'
        assert_common_properties(properties)
        assert_retro_compatibility_fields(resource)

        # AND resource_type, resource_name and resource_properties from child modules are right
        resource = resources[1]
        assert resource['resource_id'] == 'r1-addr'
        assert resource['resource_type'] == 'r1-type'
        assert resource['resource_name'] == 'cm1-addr.r1-name'

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
        tfplan_loader = TfplanLoader(tfplan_source=b'MOCKED')
        tfplan_loader.load()

        # THEN TF contents are loaded in TfplanLoader.terraform
        assert tfplan_loader.terraform
        resources = tfplan_loader.terraform['resource']
        assert len(resources) == 1

        # AND The duplicated resource is unified and the index is no present in name or id
        assert resources[0]['resource_id'] == 'r1-addr'
        assert resources[0]['resource_name'] == 'cm1-addr.r1-name'

    @patch('yaml.load')
    def test_load_modules_same_name(self, yaml_mock):
        # GIVEN a valid plain Terraform Plan file with only one module
        tfplan = build_tfplan(
            child_modules=generate_child_modules(module_count=1, resource_count=1))

        # AND two resources with the same name
        tfplan_modules = tfplan['planned_values']['root_module']['child_modules']

        original_module = tfplan_modules[0]
        duplicated_module = deepcopy(tfplan_modules[0])

        original_module['address'] = f'{original_module["address"]}["zero"]'
        original_module['resources'][0]['address'] = f'{original_module["address"]}.{original_module["resources"][0]["address"]}'

        duplicated_module['address'] = f'{duplicated_module["address"]}["one"]'
        duplicated_module['resources'][0]['address'] = f'{duplicated_module["address"]}.{duplicated_module["resources"][0]["address"]}'

        tfplan_modules.append(duplicated_module)

        yaml_mock.side_effect = [tfplan]

        # WHEN TfplanLoader::load is invoked
        tfplan_loader = TfplanLoader(tfplan_source=b'MOCKED')
        tfplan_loader.load()

        # THEN TF contents are loaded in TfplanLoader.terraform
        assert tfplan_loader.terraform
        resources = tfplan_loader.terraform['resource']
        assert len(resources) == 1

        # AND The duplicated resource is unified and the index is no present in name or id
        assert resources[0]['resource_id'] == 'cm1-addr.r1-addr'
        assert resources[0]['resource_name'] == 'cm1-addr.r1-name'

    @patch('yaml.load')
    def test_load_no_resources(self, yaml_mock):
        # GIVEN a valid Terraform Plan file with no resources
        yaml_mock.side_effect = [{'planned_values': {'root_module': {}}}]

        # WHEN TfplanLoader::load is invoked
        tfplan_loader = TfplanLoader(tfplan_source=b'MOCKED')
        tfplan_loader.load()

        # THEN TfplanLoader.terraform is an empty dictionary
        assert tfplan_loader.terraform == {}

    @patch('yaml.load')
    def test_load_empty_tfplan(self, yaml_mock):
        # GIVEN an empty TFPLAN
        yaml_mock.side_effect = [{}]

        # WHEN TfplanLoader::load is invoked
        tfplan_loader = TfplanLoader(tfplan_source=b'MOCKED')
        tfplan_loader.load()

        # THEN TfplanLoader.terraform is an empty dictionary
        assert tfplan_loader.terraform == {}

    def test_load_invalid_wrong_json(self):
        # GIVEN an invalid Terraform source file (TF or TFPLAN)
        sources = get_byte_data(INVALID_YAML)

        # WHEN TfplanLoader::load is invoked
        # THEN a LoadingIacFileError is raised
        with raises(LoadingIacFileError) as loading_error:
            TfplanLoader(sources).load()

        # AND an empty IaC file message is on the exception
        assert str(loading_error.value.title) == 'IaC file is not valid'
        assert str(loading_error.value.message) == 'The provided IaC file could not be processed'
