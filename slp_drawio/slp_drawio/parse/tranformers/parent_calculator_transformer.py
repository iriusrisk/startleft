from typing import Optional

from otm.otm.entity.parent_type import ParentType
from slp_drawio.slp_drawio.objects.diagram_objects import DiagramComponent, DiagramTrustZone
from slp_drawio.slp_drawio.parse.transformer.transformer import Transformer

PARENT_TYPES = {
    DiagramComponent: ParentType.COMPONENT,
    DiagramTrustZone: ParentType.TRUST_ZONE
}


def get_parent_type(element) -> Optional[ParentType]:
    try:
        return PARENT_TYPES[element.__class__]
    except KeyError:
        return None


class ParentCalculatorTransformer(Transformer):

    def transform(self):
        self.set_otm_parents()

    def set_otm_parents(self):
        for element in self.diagram.components + self.diagram.trustzones:
            parent_id = element.shape_parent_id
            if parent_id:
                element.otm.parent = parent_id
                parent = self.__find_by_id(parent_id)
                parent_type = get_parent_type(parent)
                element.otm.parent_type = parent_type

    def __find_by_id(self, id_: str):
        for element in self.diagram.components + self.diagram.trustzones:
            if element.otm.id == id_:
                return element
