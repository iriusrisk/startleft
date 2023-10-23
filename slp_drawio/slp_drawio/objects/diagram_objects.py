from typing import List

from otm.otm.entity import representation
from otm.otm.entity.component import Component
from otm.otm.entity.dataflow import Dataflow
from otm.otm.entity.representation import RepresentationType, RepresentationElement
from otm.otm.entity.trustzone import Trustzone


class DiagramTrustZone:
    def __init__(self, type: str, id: str = None, name: str = None, default: bool = False):
        self.otm: Trustzone = Trustzone(trustzone_id=id, name=name or '', type=type)
        self.default = default


class DiagramComponent:

    def __init__(self,
                 id: str = None,
                 name: str = None,
                 shape_type: str = None,
                 shape_parent_id: str = None,
                 representations: List[RepresentationElement] = None
                 ):
        self.otm: Component = Component(component_id=id,
                                        name=name or '',
                                        representations=representations,
                                        )
        self.shape_type = shape_type
        self.shape_parent_id = shape_parent_id

    def __str__(self) -> str:
        return '{otm: ' + str(self.otm) + '}'

    def __repr__(self) -> str:
        return '{otm: ' + str(self.otm) + '}'


class DiagramDataflow:
    def __init__(self, id: str):
        self.otm = Dataflow(dataflow_id=id, name='', source_node=None, destination_node=None)


class DiagramRepresentation:
    def __init__(self, project_id: str, size: dict):
        self.otm = representation.DiagramRepresentation(
            id_=f'{project_id}-diagram',
            name=f'{project_id} Diagram Representation',
            type_=RepresentationType.DIAGRAM,
            size=size
        )


class Diagram:
    def __init__(self,
                 representation: [DiagramRepresentation] = None,
                 components: [DiagramComponent] = None,
                 dataflows: [DiagramDataflow] = None,
                 trustzones: [DiagramTrustZone] = None,
                 default_trustzone: DiagramTrustZone = None):
        self.representation = representation
        self.components = components or []
        self.dataflows = dataflows or []
        self.trustzones = trustzones or []
        self.default_trustzone = default_trustzone
