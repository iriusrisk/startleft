import logging

from otm.otm.entity.parent_type import ParentType
from otm.otm.entity.trustzone import Trustzone
from sl_util.sl_util.str_utils import deterministic_uuid
from slp_mtmt.slp_mtmt.entity.mtmt_entity_border import MTMBorder
from slp_mtmt.slp_mtmt.mtmt_entity import MTMT
from slp_mtmt.slp_mtmt.mtmt_mapping_file_loader import MTMTMapping
from slp_mtmt.slp_mtmt.parse.mtmt_general_parser import MTMTGeneralParser
from slp_mtmt.slp_mtmt.util.trustzone_representation_calculator import TrustzoneRepresentationCalculator

DEFAULT_LABEL = 'default'
DEFAULT_NAME = 'Default trustzone'

logger = logging.getLogger(__name__)


class MTMTTrustzoneParser(MTMTGeneralParser):

    def __init__(self, source: MTMT, mapping: MTMTMapping, diagram_representation: str):
        super().__init__(source, mapping, diagram_representation)
        self.__format_legacy_mapping_tz()
        self.trustzones = []
        self.default_trustzone = self.create_default_trustzone()

    def parse(self):
        for mtmt_border in self.source.borders:
            if mtmt_border.is_trustzone:
                trustzone = self.create_trustzone(mtmt_border)
                if trustzone is not None:
                    self.trustzones.append(trustzone)
        for mtmt_line in self.source.lines:
            if mtmt_line.is_trustzone:
                trustzone = self.create_trustzone(mtmt_line)
                if trustzone is not None:
                    self.trustzones.append(trustzone)
        return self.trustzones

    def create_trustzone(self, border) -> Trustzone:
        parent = self._get_parent(border)
        if parent:
            parent_id = parent.id
            parent_type = ParentType.TRUST_ZONE if parent.is_trustzone else ParentType.COMPONENT
        else:
            parent_id, parent_type = None, None
        mtmt_type = self.__calculate_otm_type(border)
        if mtmt_type is not None:
            calculator = TrustzoneRepresentationCalculator(self.diagram_representation, border)
            representations = calculator.calculate_representation()
            tz = Trustzone(trustzone_id=border.id,
                           name=border.name,
                           type=mtmt_type,
                           parent_type=parent_type,
                           parent=parent_id,
                           attributes=border.properties)
            if representations:
                tz.representations = [representations]
            return tz

    def __calculate_otm_type(self, border: MTMBorder) -> str:
        return (self.__get_mapping_type(border.name)
                or self.__get_mapping_type(border.stencil_name)
                or self.__get_default_label_value())

    def __get_mapping_type(self, label) -> str:
        return self.__get_label_value(label, 'type')

    def __get_default_label_value(self):
        try:
            return self.mapping.mapping_trustzones[DEFAULT_LABEL]['type']
        except KeyError:
            logger.warning('Mapping file error. Any default trustzone is present')

    def __get_label_value(self, label, key):
        try:
            if label in self.mapping.mapping_trustzones:
                return self.mapping.mapping_trustzones[label][key]
        except KeyError:
            logger.warning(f'Mapping file error. The trustzone "{label}" is not present or does not has "{key}"')

    def add_default(self):
        for tz in self.trustzones:
            if tz.name == self.default_trustzone.name:
                return
        self.trustzones.append(self.default_trustzone)

    def create_default_trustzone(self):
        if self.mapping is not None and DEFAULT_LABEL in self.mapping.mapping_trustzones:
            trustzone_type = self.__get_mapping_type(DEFAULT_LABEL)
            trustzone_id = deterministic_uuid(trustzone_type)
            return Trustzone(trustzone_id=trustzone_id, type=trustzone_type, name=DEFAULT_NAME)

    def __format_legacy_mapping_tz(self):
        for k, v in self.mapping.mapping_trustzones.items():
            if 'id' in v:
                v['type'] = v.pop('id')
