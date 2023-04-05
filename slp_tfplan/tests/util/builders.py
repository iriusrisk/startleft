from copy import deepcopy
from typing import List, Dict, Tuple

from networkx import DiGraph

from otm.otm.entity.dataflow import Dataflow
from otm.otm.entity.parent_type import ParentType
from otm.otm.entity.trustzone import Trustzone
from slp_tfplan.slp_tfplan.objects.tfplan_objects import TfplanComponent, TfplanOTM, TfplanSecurityGroup, \
    TfplanLaunchTemplate

DEFAULT_TRUSTZONE = Trustzone(
    trustzone_id='default-trustzone-id',
    name='default-trustzone-name',
    type='default-trustzone-type')

TFPLAN_MINIMUM_STRUCTURE = {'planned_values': {'root_module': {}}}
MIN_FILE_SIZE = 20
MAX_TFPLAN_FILE_SIZE = 5000000  # 5MB
MAX_TFGRAPH_FILE_SIZE = 2000000 # 2MB


#######
# OTM #
#######

def build_mocked_otm(components: List[TfplanComponent],
                     dataflows: List[Dataflow] = None,
                     security_groups: List[TfplanSecurityGroup] = None,
                     launch_templates: List[TfplanLaunchTemplate] = None) -> {}:
    otm = build_base_otm(DEFAULT_TRUSTZONE)
    otm.components = components or []
    otm.security_groups = security_groups or []
    otm.launch_templates = launch_templates or []
    otm.dataflows = dataflows or []
    return otm


def build_base_otm(default_trustzone: Trustzone = None):
    otm = TfplanOTM(
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


def build_mocked_tfplan_component(component: {}) -> TfplanComponent:
    component_name = component['component_name']
    tf_type = component['tf_type']
    component_id = build_component_id(component_name, tf_type)
    return TfplanComponent(
        component_id=component_id,
        name=component_name,
        component_type=component.get('component_type', build_otm_type(tf_type)),
        parent=component.get('parent_id', DEFAULT_TRUSTZONE.id),
        parent_type=component.get('parent_type', ParentType.TRUST_ZONE),
        tags=component.get('tags', [tf_type]),
        tf_resource_id=component_id,
        tf_type=tf_type,
        configuration=component.get('configuration', {}))


def build_mocked_dataflow(
        component_a: TfplanComponent, component_b: TfplanComponent,
        bidirectional: bool = False, attributes=None, tags=None):
    return Dataflow(
        f"{component_a.id} -> {component_b.id}",
        f"{component_a.name} to {component_b.name}",
        component_a.id, component_b.id,
        bidirectional=bidirectional, attributes=attributes, tags=tags)


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

    for relationship in relationships:
        resource_id = relationship[0]
        graph.add_node(build_component_node(resource_id), label=resource_id)

    for resource_id, parent_id in relationships:
        if parent_id != DEFAULT_TRUSTZONE.id:
            graph.add_edge(build_component_node(resource_id), build_component_node(parent_id))

    return graph


###########
# GENERIC #
###########

def create_artificial_file(size: int) -> bytes:
    return bytes('A' * size, 'utf-8')
