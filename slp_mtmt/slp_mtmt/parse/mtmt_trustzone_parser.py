import logging

from otm.otm.otm import Trustzone
from sl_util.sl_util.str_utls import deterministic_uuid
from slp_mtmt.slp_mtmt.entity.mtmt_entity_border import MTMBorder
from slp_mtmt.slp_mtmt.mtmt_entity import MTMT
from slp_mtmt.slp_mtmt.mtmt_mapping_file_loader import MTMTMapping

DEFAULT_LABEL = 'default'
DEFAULT_NAME = 'Default trustzone'

logger = logging.getLogger(__name__)


class MTMTTrustzoneParser:

    def __init__(self, source: MTMT, mapping: MTMTMapping):
        self.source: MTMT = source
        self.mapping = mapping
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

    def create_trustzone(self, border: MTMBorder) -> Trustzone:
        otm_type = self.__calculate_otm_type(border)
        if otm_type is not None:
            return Trustzone(id=border.id,
                             name=border.name,
                             type=otm_type,
                             properties=border.properties)

    def __calculate_otm_type(self, border: MTMBorder) -> str:
        id = self.__get_label_value(border.stencil_name, 'id')
        if id:
            return id
        return self.__get_label_value(border.stencil_name, 'type')

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
            trustzone_type = self.mapping.mapping_trustzones[DEFAULT_LABEL]['type']
            trustzone_id = deterministic_uuid(trustzone_type)
            return Trustzone(id=trustzone_id, type=trustzone_type, name=DEFAULT_NAME)
