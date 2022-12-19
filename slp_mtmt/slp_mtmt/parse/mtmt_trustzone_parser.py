import logging

from otm.otm.entity.trustzone import OtmTrustzone
from slp_mtmt.slp_mtmt.entity.mtmt_entity_border import MTMBorder
from slp_mtmt.slp_mtmt.mtmt_entity import MTMT
from slp_mtmt.slp_mtmt.mtmt_mapping_file_loader import MTMTMapping
from slp_mtmt.slp_mtmt.util.trustzone_representation_calculator import TrustzoneRepresentationCalculator

DEFAULT_LABEL = 'default'
DEFAULT_NAME = 'Default trustzone'

logger = logging.getLogger(__name__)


class MTMTTrustzoneParser:

    def __init__(self, source: MTMT, mapping: MTMTMapping, diagram_representation: str):
        self.source: MTMT = source
        self.mapping = mapping
        self.trustzones = []
        self.default_trustzone = self.create_default_trustzone()
        self.diagram_representation = diagram_representation

    def parse(self):
        for mtmt_border in self.source.borders:
            if mtmt_border.is_trustzone:
                trustzone = self.create_border_trustzone(mtmt_border)
                if trustzone is not None:
                    self.trustzones.append(trustzone)
        for mtmt_line in self.source.lines:
            if mtmt_line.is_trustzone:
                trustzone = self.create_border_trustzone(mtmt_line)
                if trustzone is not None:
                    self.trustzones.append(trustzone)
        return self.trustzones

    def create_border_trustzone(self, border: MTMBorder) -> OtmTrustzone:
        mtmt_type = self.__calculate_otm_type(border)
        if mtmt_type is not None:
            calculator = TrustzoneRepresentationCalculator(self.diagram_representation, border)
            representations = calculator.calculate_representation()
            trustzone_id = self.calculate_otm_id(border)
            tz = OtmTrustzone(trustzone_id=trustzone_id,
                           name=border.name,
                           properties=border.properties)
            if representations:
                tz.representations = [representations]
            return tz

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

    def add_default(self):
        for tz in self.trustzones:
            if tz.name == self.default_trustzone.name:
                return
        self.trustzones.append(self.default_trustzone)

    def create_default_trustzone(self):
        if self.mapping is not None and DEFAULT_LABEL in self.mapping.mapping_trustzones:
            trustzone_id = self.mapping.mapping_trustzones[DEFAULT_LABEL]['id']
            return OtmTrustzone(trustzone_id=trustzone_id, name=DEFAULT_NAME)
