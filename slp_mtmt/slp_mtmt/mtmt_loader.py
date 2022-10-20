import collections

from slp_base.slp_base.provider_loader import ProviderLoader
from slp_mtmt.slp_mtmt.mtmt_entity import MTMT, MTMBorder, MTMLine, MTMThreat, MTMKnowledge
from slp_mtmt.slp_mtmt.tm7_to_json import Tm7ToJson


class MTMTLoader(ProviderLoader):
    """
    Builder for an MTM class from the xml data
    """

    def load(self):
        self.__read()
        self.mtmt = MTMT(borders=self.borders, lines=self.lines, threats=self.threats, know_base=self.know_base)

    def __init__(self, source):
        self.source = source
        self.borders = []
        self.lines = []
        self.threats = []
        self.know_base = {}
        self.mtmt = None

    def __read(self):
        json_ = Tm7ToJson(self.source).to_json()
        model_ = json_['ThreatModel']
        list_ = model_['DrawingSurfaceList']
        surface_model_ = list_['DrawingSurfaceModel']
        surface_model_array \
            = surface_model_ if isinstance(surface_model_, collections.abc.Sequence) else [surface_model_]

        for surface_model in surface_model_array:
            if 'Borders' in surface_model and surface_model['Borders'] is not None:
                for border in surface_model['Borders']['KeyValueOfguidanyType']:
                    self.borders.append(MTMBorder(border))
            if 'Lines' in surface_model and surface_model['Lines'] is not None:
                for line in surface_model['Lines']['KeyValueOfguidanyType']:
                    self.lines.append(MTMLine(line))

        if 'ThreatInstances' in model_ and model_['ThreatInstances'] is not None:
            for threat in model_['ThreatInstances']['KeyValueOfstringThreatpc_P0_PhOB']:
                self.threats.append(MTMThreat(threat))
        self.know_base = MTMKnowledge(model_['KnowledgeBase'])

    def get_mtmt(self) -> MTMT:
        return self.mtmt
