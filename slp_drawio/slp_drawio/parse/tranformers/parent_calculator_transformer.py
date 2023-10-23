from otm.otm.entity.parent_type import ParentType
from slp_drawio.slp_drawio.objects.diagram_objects import DiagramComponent, DiagramTrustZone
from slp_drawio.slp_drawio.parse.transformer.transformer import Transformer

PARENT_TYPES = {
    DiagramComponent: ParentType.COMPONENT,
    DiagramTrustZone: ParentType.TRUST_ZONE
}


def get_parent_type(element) -> ParentType:
    return PARENT_TYPES[element.__class__]


class ParentCalculatorTransformer(Transformer):

    def transform(self):
        self.set_otm_parents()

    def set_otm_parents(self):
        for element in self.diagram.components + self.diagram.trustzones:
            if element.shape_parent_id:
                element.otm.parent = element.shape_parent_id
                element.otm.parent_type = get_parent_type(element)
