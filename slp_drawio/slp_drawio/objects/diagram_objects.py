from otm.otm.entity.component import Component
from otm.otm.entity.dataflow import Dataflow
from otm.otm.entity.parent_type import ParentType
from otm.otm.entity.trustzone import Trustzone


class DiagramTrustZone:
    def __init__(self, id: str, name: str):
        self.otm: Trustzone = Trustzone(trustzone_id=id, name=name)


class DiagramComponent:
    def __init__(self,
                 id: str = None,
                 name: str = None):
        self.otm: Component = Component(component_id=id,
                                        name=name,
                                        component_type=None,
                                        parent_type=ParentType.TRUST_ZONE,
                                        parent=None)

    def __str__(self) -> str:
        return '{otm: ' + str(self.otm) + '}'

    def __repr__(self) -> str:
        return '{otm: ' + str(self.otm) + '}'


class DiagramDataflow:
    def __init__(self, id: str):
        self.otm = Dataflow(dataflow_id=id, source_node=None, destination_node=None)


class Diagram:
    def __init__(self,
                 components: [DiagramComponent],
                 dataflows: [DiagramDataflow],
                 trustzones: [DiagramTrustZone] = None):
        self.components = components
        self.dataflows = dataflows
        self.trustzones = trustzones or []
