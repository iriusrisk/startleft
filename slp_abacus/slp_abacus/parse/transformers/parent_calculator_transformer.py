from typing import Optional

from otm.otm.entity.parent_type import ParentType
from slp_abacus.slp_abacus.objects.diagram_objects import DiagramComponent, DiagramTrustZone
from slp_abacus.slp_abacus.parse.transformers.transformer import Transformer

PARENT_TYPES = {
    DiagramComponent: ParentType.COMPONENT,
    DiagramTrustZone: ParentType.TRUST_ZONE
}


def get_parent_type(element) -> Optional[ParentType]:
    try:
        return PARENT_TYPES[element.__class__]
    except KeyError:
        return None
