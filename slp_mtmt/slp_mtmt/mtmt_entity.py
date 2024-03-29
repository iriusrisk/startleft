from slp_mtmt.slp_mtmt.entity.mtmt_entity_border import MTMBorder
from slp_mtmt.slp_mtmt.entity.mtmt_entity_line import MTMLine
from slp_mtmt.slp_mtmt.entity.mtmt_entity_threatinstance import MTMThreat


class MTMKnowledge:
    def __init__(self, source: dict):
        pass


class MTMT:
    """
    This entity represents a Microsoft Threat Model
    """

    def __init__(self, borders: [MTMBorder], lines: [MTMLine], threats: [MTMThreat], know_base: MTMKnowledge):
        self.borders = borders
        self.lines = lines
        self.threats = threats
        self.know_base = know_base
