from otm.otm.entity.component import OtmComponent
from slp_mtmt.slp_mtmt.entity.mtmt_entity_border import MTMBorder
from slp_mtmt.slp_mtmt.mtmt_entity import MTMT
from slp_mtmt.slp_mtmt.mtmt_mapping_file_loader import MTMTMapping
from slp_mtmt.slp_mtmt.parse.mtmt_trustzone_parser import MTMTTrustzoneParser
from slp_mtmt.slp_mtmt.parse.resolvers.resolvers import get_type_resolver
from slp_mtmt.slp_mtmt.util.border_parent_calculator import BorderParentCalculator
from slp_mtmt.slp_mtmt.util.component_representation_calculator import ComponentRepresentationCalculator
from slp_mtmt.slp_mtmt.util.line_parent_calculator import LineParentCalculator


class MTMTComponentParser:

    def __init__(self, source: MTMT, mapping: MTMTMapping, trustzone_parser: MTMTTrustzoneParser,
                 diagram_representation: str):
        self.source = source
        self.mapping = mapping
        self.trustzone_parser = trustzone_parser
        self.diagram_representation = diagram_representation

    def parse(self):
        components = []
        for mtmt_border in self.source.borders:
            if mtmt_border.is_component:
                mtmt_type = self.__calculate_otm_type(mtmt_border)
                if mtmt_type is not None:
                    components.append(self.__create_component(mtmt_border))
        return components

    def __create_component(self, border: MTMBorder) -> OtmComponent:
        trustzone = self.__get_trustzone(border)
        trustzone_id = trustzone.id if trustzone else None
        if trustzone_id is None:
            trustzone_id = self.manage_orphaned()
        mtmt_type = self.__calculate_otm_type(border)
        calculator = ComponentRepresentationCalculator(self.diagram_representation, border, trustzone)
        representation = calculator.calculate_representation()
        if mtmt_type is not None:
            component = OtmComponent(component_id=border.id,
                                name=border.name,
                                component_type=mtmt_type,
                                parent_type="trustZone",
                                parent=trustzone_id,
                                properties=border.properties,
                                source=border)
            if representation:
                component.representations = [representation]
            return component

    def __calculate_otm_type(self, border: MTMBorder) -> str:
        return self.__get_label_value(border)

    def __get_label_value(self, border: MTMBorder):
        label = border.stencil_name
        if label not in self.mapping.mapping_components:
            if 'default' in self.mapping.mapping_components:
                label = 'default'
            else:
                return None
        map_ = self.mapping.mapping_components[label]

        return get_type_resolver(label).resolve(map_, border)

    def __get_trustzone(self, border: MTMBorder):
        parent_calculator = BorderParentCalculator()
        for candidate in self.source.borders:
            if parent_calculator.is_parent(candidate, border):
                return candidate
        parent_calculator = LineParentCalculator()
        for candidate in self.source.lines:
            if parent_calculator.is_parent(candidate, border):
                return candidate
        return None

    def manage_orphaned(self) -> str:
        default_trustzone = self.trustzone_parser.default_trustzone
        if default_trustzone is not None:
            self.trustzone_parser.add_default()
            return default_trustzone.id
