from networkx import DiGraph

from otm.otm.entity.trustzone import OtmTrustzone
from otm.otm.otm_builder import OtmBuilder
from slp_base import IacType
from slp_tf.slp_tf.tfplan.tfplan_component import TfplanComponent

DEFAULT_TRUSTZONE = OtmTrustzone(
    trustzone_id='default-trustzone-id',
    name='default-trustzone-name',
    type='default-trustzone-type')


def build_base_otm(default_trustzone: OtmTrustzone = None):
    otm_builder = OtmBuilder('project_id', 'project_name', IacType.TERRAFORM)
    if default_trustzone:
        otm_builder.add_default_trustzone(default_trustzone)

    return otm_builder.build()


def build_component_node(component_id: str) -> str:
    return f'[root] {component_id} (expand)'


def build_component_id(base_name: str, component_type: str) -> str:
    return f'{component_type}.{base_name}'


def build_otm_type(component_type: str) -> str:
    return f'{component_type}-otm-type'


def build_mocked_otm(component_types_names: {}) -> {}:
    otm = build_base_otm(DEFAULT_TRUSTZONE)

    for component_name, component_type in component_types_names.items():
        component_id = build_component_id(component_name, component_type)

        otm.components.append(
            TfplanComponent(
                component_id=component_id,
                name=component_name,
                component_type=build_otm_type(component_name),
                parent=DEFAULT_TRUSTZONE.id,
                parent_type='trustZone',
                tags=[component_type],
                tf_resource_id=component_id,
                tf_type=component_type))

    return otm


def build_graph(relationships: [()]):
    graph = DiGraph()

    for relationship in relationships:
        resource_id = relationship[0]
        graph.add_node(build_component_node(resource_id), label=resource_id)

    for resource_id, parent_id in relationships:
        if parent_id != DEFAULT_TRUSTZONE.id:
            graph.add_edge(build_component_node(resource_id), build_component_node(parent_id))

    return graph


def assert_parents(components: [TfplanComponent], relationships: dict = None):
    for component in components:
        assert_parent(component=component, parent_id=relationships.get(component.id))


def assert_parent(component: TfplanComponent, parent_id: str = None):
    if parent_id:
        assert component.parent_type == 'component'
        assert component.parent == parent_id
    else:
        assert component.parent_type == 'trustZone'
        assert component.parent == DEFAULT_TRUSTZONE.id
