from typing import List

from otm.otm.entity import representation
from otm.otm.entity.component import Component
from otm.otm.entity.dataflow import Dataflow
from otm.otm.entity.representation import RepresentationType, RepresentationElement
from otm.otm.entity.trustzone import Trustzone
from sl_util.sl_util.lang_utils import auto_repr


@auto_repr
class DiagramTrustZone:
    def __init__(self, type_: str, id_: str = None, name: str = None, default: bool = False, shape_parent_id=None,
                 shape_type: str = None, representations: List[RepresentationElement] = None):
        self.otm: Trustzone = Trustzone(trustzone_id=id_, name=name or '', type=type_, representations=representations)
        self.default = default
        self.shape_parent_id = shape_parent_id
        self.shape_type = shape_type


@auto_repr
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
                                        representations=representations
                                        )
        self.shape_type = shape_type
        self.shape_parent_id = shape_parent_id

    def __str__(self) -> str:
        return f'{{otm: {str(self.otm)}, shape_type: {self.shape_type}, shape_parent_id: {self.shape_parent_id}}}'


@auto_repr
class DiagramDataflow:
    def __init__(self,
                 dataflow_id: str,
                 name: str = '',
                 source_node: str = None,
                 destination_node: str = None,
                 tags: List[str] = None
                 ):
        self.otm = Dataflow(
            dataflow_id=dataflow_id,
            name=name,
            source_node=source_node,
            destination_node=destination_node,
            tags=tags
        )


@auto_repr
class DiagramRepresentation:
    def __init__(self, project_id: str, size: dict):
        self.otm = representation.DiagramRepresentation(
            id_=f'{project_id}-diagram',
            name=f'{project_id} Diagram Representation',
            type_=RepresentationType.DIAGRAM,
            size=size
        )


@auto_repr
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
