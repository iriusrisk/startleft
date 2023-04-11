import random
from copy import deepcopy
from json import JSONDecodeError
from typing import List
from unittest.mock import patch, Mock

from networkx import DiGraph
from pytest import raises, mark, param, fixture

from slp_tfplan.slp_tfplan.load.tfplan_loader import TFPlanLoader
from slp_tfplan.tests.resources import test_resource_paths
from slp_base import LoadingIacFileError
from slp_tfplan.tests.util.builders import build_tfplan, generate_resources, generate_child_modules
from slp_tfplan.tests.util.asserts import assert_common_properties
from sl_util.sl_util.str_utils import get_bytes

INVALID_YAML = test_resource_paths.invalid_yaml
TF_FILE_YAML_EXCEPTION = JSONDecodeError('HLC2 cannot be processed as JSON', doc='sample-doc', pos=0)


@fixture
def mock_load_tfplan(mocker, mocked_tfplan):
    mocker.patch('yaml.load', side_effect=mocked_tfplan)


@fixture(autouse=True)
def mocked_graph():
    yield Mock()


@fixture(autouse=True)
def mock_load_graph(mocker, mocked_graph):
    mocker.patch('slp_tfplan.slp_tfplan.load.tfplan_loader.load_tfgraph', side_effect=mocked_graph)


class TestTFPlanLoader:

    @patch('slp_tfplan.slp_tfplan.load.tfplan_loader.load_tfgraph')
    @patch('yaml.load')
    def test_load_tfplan_and_graph(self, yaml_mock, from_agraph_mock):
        # GIVEN a valid plain Terraform Plan file with no modules
        yaml_mock.side_effect = [build_tfplan(resources=generate_resources(2))]

        # AND a mocked graph load result
        graph_label = 'Mocked Graph'
        from_agraph_mock.side_effect = [DiGraph(label=graph_label)]

        # WHEN TFPlanLoader::load is invoked
        tfplan_loader = TFPlanLoader(sources=[b'MOCKED', b'MOCKED'])
        tfplan_loader.load()

        # THEN the TFPLAN is loaded
        assert tfplan_loader.get_terraform() is not None

        # AND the TFGRAPH is also loaded
        assert tfplan_loader.get_tfgraph().graph['label'] == graph_label

    @patch('yaml.load')
    def test_load_no_modules(self, yaml_mock):
        # GIVEN a valid plain Terraform Plan file with no modules
        yaml_mock.side_effect = [build_tfplan(resources=generate_resources(2))]

        # WHEN TFPlanLoader::load is invoked
        tfplan_loader = TFPlanLoader(sources=[b'MOCKED', b'MOCKED'])
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
            assert properties['resource_address'] == f'r{i}-addr'

    @patch('yaml.load')
    def test_load_only_modules(self, yaml_mock):
        # GIVEN a valid plain Terraform Plan file with only modules
        yaml_mock.side_effect = [build_tfplan(
            child_modules=generate_child_modules(module_count=2, resource_count=2))]

        # WHEN TFPlanLoader::load is invoked
        tfplan_loader = TFPlanLoader(sources=[b'MOCKED', b'MOCKED'])
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

                resource_index += 1

    @patch('yaml.load')
    def test_load_nested_modules(self, yaml_mock):
        # GIVEN a valid plain Terraform Plan file with nested modules
        yaml_mock.side_effect = [build_tfplan(
            child_modules=generate_child_modules(
                module_count=1,
                child_modules=generate_child_modules(module_count=1, resource_count=1)))]

        # WHEN TFPlanLoader::load is invoked
        tfplan_loader = TFPlanLoader(sources=[b'MOCKED', b'MOCKED'])
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

    @patch('yaml.load')
    def test_load_complex_structure(self, yaml_mock):
        # GIVEN a valid plain Terraform Plan file with modules and root-level resources
        yaml_mock.side_effect = [build_tfplan(
            resources=generate_resources(1),
            child_modules=generate_child_modules(module_count=1, resource_count=1))]

        # WHEN TFPlanLoader::load is invoked
        tfplan_loader = TFPlanLoader(sources=[b'MOCKED', b'MOCKED'])
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

        # AND resource_type, resource_name and resource_properties from child modules are right
        resource = resources[1]
        assert resource['resource_id'] == 'r1-addr'
        assert resource['resource_type'] == 'r1-type'
        assert resource['resource_name'] == 'cm1-addr.r1-name'

        properties = resource['resource_properties']
        assert properties['resource_address'] == 'r1-addr'
        assert_common_properties(properties)

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

        # WHEN TFPlanLoader::load is invoked
        tfplan_loader = TFPlanLoader(sources=[b'MOCKED', b'MOCKED'])
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
        original_module['resources'][0][
            'address'] = f'{original_module["address"]}.{original_module["resources"][0]["address"]}'

        duplicated_module['address'] = f'{duplicated_module["address"]}["one"]'
        duplicated_module['resources'][0][
            'address'] = f'{duplicated_module["address"]}.{duplicated_module["resources"][0]["address"]}'

        tfplan_modules.append(duplicated_module)

        yaml_mock.side_effect = [tfplan]

        # WHEN TFPlanLoader::load is invoked
        tfplan_loader = TFPlanLoader(sources=[b'MOCKED', b'MOCKED'])
        tfplan_loader.load()

        # THEN TF contents are loaded in TfplanLoader.terraform
        assert tfplan_loader.terraform
        resources = tfplan_loader.terraform['resource']
        assert len(resources) == 1

        # AND The duplicated resource is unified and the index is not present in name or id
        assert resources[0]['resource_id'] == 'cm1-addr.r1-addr'
        assert resources[0]['resource_name'] == 'cm1-addr.r1-name'

    @patch('yaml.load')
    def test_load_no_resources(self, yaml_mock):
        # GIVEN a valid Terraform Plan file with no resources
        yaml_mock.side_effect = [{'planned_values': {'root_module': {}}}]

        # WHEN TFPlanLoader::load is invoked
        tfplan_loader = TFPlanLoader(sources=[b'MOCKED', b'MOCKED'])
        tfplan_loader.load()

        # THEN TfplanLoader.terraform is an empty dictionary
        assert tfplan_loader.terraform == {}

    @patch('yaml.load')
    def test_load_empty_tfplan(self, yaml_mock):
        # GIVEN an empty TFPLAN
        yaml_mock.side_effect = [{}]

        # WHEN TFPlanLoader::load is invoked
        tfplan_loader = TFPlanLoader(sources=[b'MOCKED', b'MOCKED'])
        tfplan_loader.load()

        # THEN TfplanLoader.terraform is an empty dictionary
        assert tfplan_loader.terraform == {}

    @mark.parametrize('sources', [
        param([], id='no sources'),
        param([b'MOCKED'], id='one source'),
        param([b'MOCKED'] * random.randint(3, 10), id='more than two sources')
    ])
    def test_load_invalid_number_of_sources(self, sources: List[bytes]):
        # GIVEN an invalid number of sources

        # WHEN TFPlanLoader::load is invoked
        # THEN a LoadingIacFileError is raised
        with raises(LoadingIacFileError) as error:
            TFPlanLoader(sources=sources).load()

        # AND an empty IaC file message is on the exception
        assert error.value.title == 'Wrong number of files'
        assert error.value.message == 'Required one tfplan and one tfgraph files'

    @mark.usefixtures('mock_load_tfplan')
    @mark.parametrize('mocked_tfplan,mocked_graph', [
        param([None], [None], id='no valid sources'),
        param([None, None], [Mock()], id='no tfplan'),
        param([Mock()], [None], id='no tfgraph')
    ])
    def test_load_invalid_sources(self, mocked_tfplan, mocked_graph):
        # GIVEN mocked invalid results for loading tfplan and tfgraph

        # WHEN TFPlanLoader::load is invoked
        # THEN a LoadingIacFileError is raised
        with raises(LoadingIacFileError) as error:
            TFPlanLoader(sources=[get_bytes('MOCKED')] * 2).load()

        # AND an empty IaC file message is on the exception
        assert str(error.value.title) == 'IaC files are not valid'
        assert str(error.value.message) == 'The provided IaC files could not be processed'
