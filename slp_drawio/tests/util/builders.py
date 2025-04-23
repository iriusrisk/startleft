from typing import List

from slp_drawio.slp_drawio.objects.diagram_objects import DiagramComponent, Diagram, DiagramTrustZone, \
    DiagramRepresentation


def build_diagram(default_trustzone: DiagramTrustZone = None, trustzones: List[DiagramTrustZone] = None,
                  components: List[DiagramComponent] = None):
    return Diagram(
        default_trustzone=default_trustzone,
        trustzones=trustzones,
        components=components,
        representation=DiagramRepresentation('repr-id', {'heigh': 1000, 'width': 1000}))


def build_trustzone(trustzone_id: str = 'tz-id', type: str = 'tz-type', name: str = None, default: bool = False):
    return DiagramTrustZone(id=trustzone_id, name=name or f'{trustzone_id} name', type=type, default=default)


def build_component(component_id: str = 'c-id', parent_id: str = None, name: str = None, shape_type: str = None) -> DiagramComponent:
    component = DiagramComponent(id=component_id, name=name)
    component.otm.parent = parent_id
    component.shape_type = shape_type
    return component


def build_components(count: int, orphan: bool = False) -> List[DiagramComponent]:
    return list(map(
        lambda c_id: build_component(f'{c_id}', None if orphan else f'p-{c_id}'),
        range(1, count + 1)))
