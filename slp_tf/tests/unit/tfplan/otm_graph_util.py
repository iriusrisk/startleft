from typing import List

from networkx import DiGraph

from otm.otm.entity.dataflow import Dataflow
from otm.otm.entity.parent_type import ParentType
from otm.otm.entity.trustzone import Trustzone
from otm.otm.otm_builder import OTMBuilder
from slp_base import IacType
from slp_tf.slp_tf.tfplan.tfplan_component import TfplanComponent

DEFAULT_TRUSTZONE = Trustzone(
    trustzone_id='default-trustzone-id',
    name='default-trustzone-name',
    type='default-trustzone-type')


def build_base_otm(default_trustzone: Trustzone = None):
    otm_builder = OTMBuilder('project_id', 'project_name', IacType.TERRAFORM)
    if default_trustzone:
        otm_builder.add_default_trustzone(default_trustzone)

    return otm_builder.build()


def build_component_node(component_id: str) -> str:
    return f'[root] {component_id} (expand)'


def build_component_id(base_name: str, component_type: str) -> str:
    return f'{component_type}.{base_name}'


def build_otm_type(component_type: str) -> str:
    return f'{component_type}-otm-type'


def build_mocked_otm(components: List[TfplanComponent], dataflows: List[Dataflow] = None) -> {}:
    otm = build_base_otm(DEFAULT_TRUSTZONE)
    otm.components = components
    otm.dataflows = dataflows
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
        assert component.parent_type == ParentType.COMPONENT
        assert component.parent == parent_id
    else:
        assert component.parent_type == ParentType.TRUST_ZONE
        assert component.parent == DEFAULT_TRUSTZONE.id