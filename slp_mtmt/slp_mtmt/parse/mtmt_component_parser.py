from otm.otm.otm import Component
from slp_mtmt.slp_mtmt.entity.mtmt_entity_border import MTMBorder
from slp_mtmt.slp_mtmt.mtmt_entity import MTMT
from slp_mtmt.slp_mtmt.mtmt_mapping_file_loader import MTMTMapping
from slp_mtmt.slp_mtmt.util.border_parent_calculator import BorderParentCalculator


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

    def __create_component(self, border: MTMBorder) -> Component:
        trustzone_id = self.__get_trustzone_id(border)
        mtmt_type = self.__calculate_otm_type(border.name)
        if mtmt_type is not None:
            return Component(id=border.id,
                             name=border.name,
                             type=mtmt_type,
                             parent_type="trustZone",
                             parent=trustzone_id,
                             properties=border.properties)

    def __calculate_otm_type(self, component_type: str) -> str:
        return self.__find_mapped_component_by_label(component_type)

    def __find_mapped_component_by_label(self, label: str) -> str:
        return self.mapping.mapping_components[label]['type'] if label in self.mapping.mapping_components \
            else None

    def __get_trustzone_id(self, border: MTMBorder):
        parent_calculator = BorderParentCalculator()
        for candidate in self.source.borders:
            if parent_calculator.is_parent(candidate, border):
                return candidate.id
        return ""
