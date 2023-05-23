from copy import deepcopy
from typing import List, Dict, Tuple, Type
from unittest.mock import Mock

from dependency_injector import providers
from networkx import DiGraph

from otm.otm.entity.dataflow import Dataflow
from otm.otm.entity.parent_type import ParentType
from otm.otm.entity.trustzone import Trustzone
from slp_tfplan.slp_tfplan.objects.tfplan_objects import TFPlanComponent, TFPlanOTM, SecurityGroup, \
    LaunchTemplate

DEFAULT_TRUSTZONE = Trustzone(
    trustzone_id='default-trustzone-id',
    name='default-trustzone-name',
    type='default-trustzone-type')

TFPLAN_MINIMUM_STRUCTURE = {'planned_values': {'root_module': {}}}
MIN_FILE_SIZE = 20
MAX_TFPLAN_FILE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_TFGRAPH_FILE_SIZE = 2 * 1024 * 1024  # 2MB


#######
# OTM #
#######

def build_mocked_otm(components: List[TFPlanComponent],
                     dataflows: List[Dataflow] = None,
                     security_groups: List[SecurityGroup] = None,
                     launch_templates: List[LaunchTemplate] = None) -> {}:
    otm = build_base_otm(DEFAULT_TRUSTZONE)
    otm.components = components or []
    otm.security_groups = security_groups or []
    otm.launch_templates = launch_templates or []
    otm.dataflows = dataflows or []
    return otm


def build_base_otm(default_trustzone: Trustzone = None):
    otm = TFPlanOTM(
        project_id='project_id',
        project_name='project_name',
        components=[],
        security_groups=[],
        launch_templates=[],
        dataflows=[],
    )
    if default_trustzone:
        otm.default_trustzone = default_trustzone

    return otm


def build_mocked_component(component: Dict) -> TFPlanComponent:
    component_name = component['component_name']
    tf_type = component['tf_type']
    component_id = component.get('id', build_component_id(component_name, tf_type))

    return TFPlanComponent(
        component_id=component_id,
        name=component_name,
        component_type=component.get('component_type', build_otm_type(tf_type)),
        parent=component.get('parent_id', DEFAULT_TRUSTZONE.id),
        parent_type=component.get('parent_type', ParentType.TRUST_ZONE),
        tags=component.get('tags', [tf_type]),
        tf_resource_id=component_id,
        tf_type=tf_type,
        configuration=component.get('configuration', {}),
        clones_ids=component.get('clones_ids', [])
    )

def build_simple_mocked_component(id: str, parent: str = None, clones_ids: List[str] = None) -> Mock:
    c = Mock(id=id, tf_resource_id=id, clones_ids=clones_ids)
    c.name = id

    if parent:
        c.parent_type = ParentType.COMPONENT
        c.parent = parent

    return c


def build_mocked_dataflow(
        component_a: TFPlanComponent, component_b: TFPlanComponent,
        bidirectional: bool = False, attributes=None, tags=None):
    return Dataflow(
        f"{component_a.id} -> {component_b.id}",
        f"{component_a.name} to {component_b.name}",
        component_a.id, component_b.id,
        bidirectional=bidirectional, attributes=attributes, tags=tags)


def build_security_group_mock(id: str, ingres_sgs: List[str] = None, egress_sgs: List[str] = None):
    return Mock(security_group_id=id, ingres_sgs=ingres_sgs, egress_sgs=egress_sgs)


def build_component_node(component_id: str) -> str:
    return f'[root] {component_id} (expand)'


def build_component_id(base_name: str, component_type: str) -> str:
    return f'{component_type}.{base_name}'


def build_otm_type(component_type: str) -> str:
    return f'{component_type}-otm-type'


##########
# TFPLAN #
##########

def build_tfplan(resources: List[Dict] = None, child_modules: List[Dict] = None) -> {}:
    tfplan = deepcopy(TFPLAN_MINIMUM_STRUCTURE)

    if resources:
        tfplan['planned_values']['root_module']['resources'] = resources

    if child_modules:
        tfplan['planned_values']['root_module']['child_modules'] = child_modules

    return tfplan


def generate_resources(resource_count: int, module_child: bool = False) -> List[Dict]:
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


def generate_child_modules(module_count: int,
                           child_modules: List[Dict] = None,
                           resource_count: int = None) -> List[Dict]:
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


###########
# TFGRAPH #
###########


def build_tfgraph(relationships: List[Tuple] = None) -> DiGraph:
    graph = DiGraph()

    if not relationships:
        return graph

    _create_graph_nodes(graph, relationships)

    for resource_id, parent_id in relationships:
        if parent_id != DEFAULT_TRUSTZONE.id:
            graph.add_edge(build_component_node(resource_id), build_component_node(parent_id))

    return graph


def _create_graph_nodes(graph: DiGraph, relationships: List[Tuple]):
    [graph.add_node(build_component_node(resource_id), label=resource_id)
     for resource_id in set([resource_id for relationship in relationships for resource_id in relationship])]


###########
# GENERIC #
###########

def create_artificial_file(size: int) -> bytes:
    return bytes('A' * size, 'utf-8')


def get_instance_classes(instances: providers.List) -> List[Type]:
    return [instance.cls for instance in list(instances.args)]


##########
# ERRORS #
##########

class MockedException(Exception):
    def __init__(self, message):
        self.message = message
