from typing import List, Union

from otm.otm.entity.parent_type import ParentType
from otm.otm.trustzone_representation_calculator import \
    TrustZoneRepresentationCalculator
from sl_util.sl_util.iterations_utils import append_if_not_exists
from slp_base import OTMBuildingError
from slp_drawio.slp_drawio.objects.diagram_objects import Diagram, DiagramTrustZone, DiagramComponent
from slp_drawio.slp_drawio.parse.transformer.transformer import Transformer


def _find_orphan_components(components: List[DiagramComponent]) -> List[DiagramComponent]:
    return list(filter(lambda c: not c.otm.parent, components))


class DefaultTrustZoneTransformer(Transformer):
    def __init__(self, diagram: Diagram):
        super().__init__(diagram)

        self.orphan_components: List[DiagramComponent] = _find_orphan_components(self.diagram.components)
        self.default_trustzone: DiagramTrustZone = self.diagram.default_trustzone

    def transform(self):
        if not self.orphan_components:
            return

        if not self.default_trustzone:
            raise OTMBuildingError(title='Invalid configuration', message='A default trust zone is required with orphan components')

        self.__use_default_trustzone_as_global_parent()

    def __use_default_trustzone_as_global_parent(self):
        append_if_not_exists(self.default_trustzone, self.diagram.trustzones)

        orphans = self.orphan_components + self.__get_orphan_trustzones_excluding_default()
        self.__set_default_trustzone_as_parent(orphans)
        self.__recalculate_representations(orphans)

    def __set_default_trustzone_as_parent(self, orphans: List[Union[DiagramComponent, DiagramTrustZone]]):
        for orphan in orphans:
            orphan.otm.parent_type = ParentType.TRUST_ZONE
            orphan.otm.parent = self.default_trustzone.otm.id

    def __recalculate_representations(self, children: List[Union[DiagramComponent, DiagramTrustZone]]):
        TrustZoneRepresentationCalculator(representation_id=self.diagram.representation.id,
                                          trustzone=self.default_trustzone.otm,
                                          children=[c.otm for c in children]).calculate()

    def __get_orphan_trustzones_excluding_default(self) -> List[DiagramTrustZone]:
        return list(filter(lambda tz: not tz.otm.parent and tz != self.default_trustzone, self.diagram.trustzones))
