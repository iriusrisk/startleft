from otm.otm.entity.component import Component
from otm.otm.entity.parent_type import ParentType
from slp_mtmt.slp_mtmt.entity.mtmt_entity_border import MTMBorder
from slp_mtmt.slp_mtmt.mtmt_entity import MTMT
from slp_mtmt.slp_mtmt.mtmt_mapping_file_loader import MTMTMapping
from slp_mtmt.slp_mtmt.parse.mtmt_general_parser import MTMTGeneralParser
from slp_mtmt.slp_mtmt.parse.mtmt_trustzone_parser import MTMTTrustzoneParser
from slp_mtmt.slp_mtmt.parse.resolvers.resolvers import get_type_resolver
from slp_mtmt.slp_mtmt.util.component_representation_calculator import ComponentRepresentationCalculator


class MTMTComponentParser(MTMTGeneralParser):

    def __init__(self, source: MTMT, mapping: MTMTMapping, trustzone_parser: MTMTTrustzoneParser,
                 diagram_representation: str):
        super().__init__(source, mapping, diagram_representation)
        self.trustzone_parser = trustzone_parser

    def parse(self):
        components = []
        for mtmt_border in self.source.borders:
            if mtmt_border.is_component:
                mtmt_type = self.__calculate_otm_type(mtmt_border)
                if mtmt_type is not None:
                    components.append(self.__create_component(mtmt_border))
        return components

    def __create_component(self, border: MTMBorder) -> Component:
        parent = self._get_parent(border)
        if parent:
            parent_type = ParentType.TRUST_ZONE if parent.is_trustzone else ParentType.COMPONENT
        else:
            parent = self.manage_orphaned()
            parent_type = ParentType.TRUST_ZONE
        parent_id = parent.id if parent else None
        mtmt_type = self.__calculate_otm_type(border)
        calculator = ComponentRepresentationCalculator(self.diagram_representation, border, parent)
        representation = calculator.calculate_representation()
        if mtmt_type is not None:
            component = Component(component_id=border.id,
                                  name=border.name or '',
                                  component_type=mtmt_type,
                                  parent_type=parent_type,
                                  parent=parent_id,
                                  attributes=border.properties,
                                  source=border)
            if representation:
                calculator.scale_representation(representation)
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

    def manage_orphaned(self) -> str:
        default_trustzone = self.trustzone_parser.default_trustzone
        if default_trustzone is not None:
            self.trustzone_parser.add_default()
            return default_trustzone
