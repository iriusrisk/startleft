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
        if mtmt_type is not None:
            return Trustzone(id=border.id,
                             name=border.name,
                             properties=border.properties)

    def __calculate_otm_type(self, label: str) -> str:
        return self.mapping.mapping_trustzones[label]['type'] if label in self.mapping.mapping_trustzones \
            else None

    def parse_default_trustzone(self) -> Trustzone:
        return Trustzone("b61d6911-338d-46a8-9f39-8dcd24abfe91", "Public Cloud")
