from otm.otm.otm import Component, Trustzone
from slp_mtmt.slp_mtmt.entity.mtmt_entity_border import MTMBorder
from slp_mtmt.slp_mtmt.mtmt_entity import MTMT
from slp_mtmt.slp_mtmt.mtmt_mapping_file_loader import MTMTMapping


class MTMTComponentParser:

    def __init__(self, source: MTMT, mapping: MTMTMapping):
        self.source = source
        self.mapping = mapping

    def parse(self):
        components = []
        for mtmt_border in self.source.borders:
            if mtmt_border.is_component:
                mtmt_type = self.__calculate_otm_type(mtmt_border.name)
                if mtmt_type is not None:
                    components.append(self.__create_component(mtmt_border))
        return components

    def __create_component(self, mtmt: MTMBorder) -> Component:
        trustzone = self.get_default_trustzone()
        mtmt_type = self.__calculate_otm_type(mtmt.name)
        if mtmt_type is not None:
            return Component(id=mtmt.id,
                             name=mtmt.name,
                             type=mtmt_type,
                             # TODO implements parents field in OPT-315
                             parent_type="trustZone",
                             parent=trustzone.id,
                             properties=mtmt.properties)

    def __calculate_otm_type(self, component_type: str) -> str:
        return self.__find_mapped_component_by_label(component_type)

    def __find_mapped_component_by_label(self, label: str) -> str:
        return self.mapping.mapping_components[label]['type'] if label in self.mapping.mapping_components \
            else None

    @staticmethod
    def get_default_trustzone():
        return Trustzone("b61d6911-338d-46a8-9f39-8dcd24abfe91", "Public Cloud")
