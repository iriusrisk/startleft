from otm.otm.otm import Trustzone
from slp_mtmt.slp_mtmt.entity.mtmt_entity_border import MTMBorder
from slp_mtmt.slp_mtmt.mtmt_entity import MTMT
from slp_mtmt.slp_mtmt.mtmt_mapping_file_loader import MTMTMapping


class MTMTTrustzoneParser:

    def __init__(self, source: MTMT, mapping: MTMTMapping):
        self.source: MTMT = source
        self.mapping = mapping

    def parse(self):
        trustzones = []
        for mtmt_border in self.source.borders:
            if mtmt_border.is_trustzone:
                mtmt_type = self.__calculate_otm_type(mtmt_border.name)
                if mtmt_type is not None:
                    trustzones.append(self.__create_trustzone(mtmt_border))
        return trustzones

    def __create_trustzone(self, border: MTMBorder) -> Trustzone:
        mtmt_type = self.__calculate_otm_type(border.name)
        trustzone_id = self.calculate_otm_id(border.name)
        if mtmt_type is not None:
            return Trustzone(id=trustzone_id,
                             name=border.name,
                             properties=border.properties)

    def __calculate_otm_type(self, label: str) -> str:
        return self.__get_label_value(label, 'type')

    def calculate_otm_id(self, label: str) -> str:
        return self.__get_label_value(label, 'id')

    def __get_label_value(self, label, key):
        return self.mapping.mapping_trustzones[label][key] if label in self.mapping.mapping_trustzones \
            else None
