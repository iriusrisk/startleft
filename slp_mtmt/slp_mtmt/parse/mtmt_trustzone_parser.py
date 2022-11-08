import logging

from otm.otm.otm import Trustzone
from slp_mtmt.slp_mtmt.entity.mtmt_entity_border import MTMBorder
from slp_mtmt.slp_mtmt.mtmt_entity import MTMT
from slp_mtmt.slp_mtmt.mtmt_mapping_file_loader import MTMTMapping
from slp_mtmt.slp_mtmt.util.component_representation_calculator import ComponentRepresentationCalculator

calculate_representation = ComponentRepresentationCalculator.calculate_representation

DEFAULT_LABEL = 'default'

logger = logging.getLogger(__name__)


class MTMTTrustzoneParser:

    def __init__(self, source: MTMT, mapping: MTMTMapping, diagram_representation: str):
        self.source: MTMT = source
        self.mapping = mapping
        self.diagram_representation = diagram_representation

    def parse(self):
        trustzones = []
        for mtmt_border in self.source.borders:
            if mtmt_border.is_trustzone:
                trustzone = self.create_trustzone(mtmt_border)
                if trustzone is not None:
                    trustzones.append(trustzone)
        return trustzones

    def create_trustzone(self, border: MTMBorder) -> Trustzone:
        mtmt_type = self.__calculate_otm_type(border)
        representations = calculate_representation(border, self.diagram_representation)
        if mtmt_type is not None:
            trustzone_id = self.calculate_otm_id(border)
            return Trustzone(id=trustzone_id,
                             name=border.name,
                             properties=border.properties,
                             representations=[representations])

    def __calculate_otm_type(self, border: MTMBorder) -> str:
        return self.__get_label_value(border.stencil_name, 'type')

    def calculate_otm_id(self, border: MTMBorder) -> str:
        return self.__get_label_value(border.stencil_name, 'id')

    def __get_label_value(self, label, key):
        try:
            if label in self.mapping.mapping_trustzones:
                return self.mapping.mapping_trustzones[label][key]
            else:
                return self.mapping.mapping_trustzones[DEFAULT_LABEL][key]
        except KeyError:
            logger.warning(f'Mapping file error. The trustzone "{label}" is not present or does not has '
                           f' "{key}" and any default trustzone is present')

        return None
