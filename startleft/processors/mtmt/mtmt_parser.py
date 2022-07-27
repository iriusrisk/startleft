from startleft.processors.base.provider_parser import ProviderParser
from startleft.processors.mtmt.mtmt_entity import MTMT


class MTMTParser(ProviderParser):
    """
    Parser to build an OTM from Microsoft Threat Model
    """

    def __init__(self, source: MTMT, mapping: [str]):
        self.source = source
        self.mapping = mapping

    def build_otm(self) -> dict:
        raise NotImplementedError
