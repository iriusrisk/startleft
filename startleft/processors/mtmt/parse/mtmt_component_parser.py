from startleft.otm.otm import Component, Trustzone
from startleft.processors.mtmt.entity.mtmt_entity_border import MTMBorder
from startleft.processors.mtmt.mtmt_entity import MTMT


def get_default_trustzone():
    return Trustzone("b61d6911-338d-46a8-9f39-8dcd24abfe91", "Public Cloud")


class MTMTComponentParser:

    def __init__(self, source: MTMT, mapping: [str]):
        self.source = source
        self.mapping = mapping

    def parse(self):
        components = []
        for mtmt_border in self.source.borders:
            if mtmt_border.is_component:
                components.append(self.create_component(mtmt_border))
        return components

    def create_component(self, mtmt: MTMBorder) -> Component:
        trustzone = get_default_trustzone()
        return Component(id=mtmt.id,
                         name=mtmt.name,
                         type=mtmt.type,
                         # TODO implements parents field in OPT-315
                         parent_type="trustZone",
                         parent=trustzone.id,
                         properties=mtmt.properties)

   
