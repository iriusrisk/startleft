class MTMBorder:
    def __init__(self, source: dict):
        raise NotImplementedError

    def get_components(self):
        raise NotImplementedError

    def get_trustzones(self):
        raise NotImplementedError


class MTMLine:
    def __init__(self, source: dict):
        raise NotImplementedError

    def get_dataflows(self):
        raise NotImplementedError

    def get_trustzones(self):
        raise NotImplementedError


class MTMThreat:
    def __init__(self, source: dict):
        raise NotImplementedError


class MTMKnowledge:
    def __init__(self, source: dict):
        raise NotImplementedError


class MTMT:
    """
    This entity represents a Microsoft Threat Model
    """

    def __init__(self, borders: [MTMBorder], lines: [MTMLine], threats: [MTMThreat], know_base: MTMKnowledge):
        self.borders = borders
        self.lines = lines
        self.threats = threats
        self.know_base = know_base

