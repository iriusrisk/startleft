import collections
import logging

from slp_base import LoadingSourceFileError
from slp_base.slp_base.provider_loader import ProviderLoader
from slp_mtmt.slp_mtmt.entity.mtmt_entity_threatinstance import MTMThreat
from slp_mtmt.slp_mtmt.mtmt_entity import MTMT, MTMBorder, MTMLine, MTMKnowledge
from slp_mtmt.slp_mtmt.tm7_to_dict import Tm7ToDict

logger = logging.getLogger(__name__)


class MTMTLoader(ProviderLoader):
    """
    Builder for an MTM class from the xml data
    """

    def load(self):
        try:
            self.__read()
            self.mtmt = MTMT(borders=self.borders, lines=self.lines, threats=self.threats, know_base=self.know_base)
        except Exception as e:
            logger.error(f'{e}')
            detail = e.__class__.__name__
            message = e.__str__()
            raise LoadingSourceFileError('Source file cannot be loaded', detail, message)

    def __init__(self, source):
        self.source = source
        self.borders = []
        self.lines = []
        self.threats = []
        self.know_base = {}
        self.mtmt = None

    def __read(self):
        json_ = Tm7ToDict(self.source).to_dict()
        model_ = json_['ThreatModel']
        list_ = model_['DrawingSurfaceList']
        surface_model_ = list_['DrawingSurfaceModel']
        surface_model_ \
            = surface_model_[0] if isinstance(surface_model_, collections.abc.Sequence) else surface_model_

        # Only the first tab of the MTMT file is processed
        self.add_borders(surface_model_)
        self.add_lines(surface_model_)

        self.add_threats(model_)
        self.know_base = MTMKnowledge(model_['KnowledgeBase'])

    def add_threats(self, model_):
        if 'ThreatInstances' in model_ and model_['ThreatInstances'] is not None:
            for threat in model_['ThreatInstances']['KeyValueOfstringThreatpc_P0_PhOB']:
                self.threats.append(MTMThreat(threat))

    def add_lines(self, surface_model):
        if 'Lines' in surface_model and surface_model['Lines'] is not None:
            for line in surface_model['Lines']['KeyValueOfguidanyType']:
                self.lines.append(MTMLine(line))

    def add_borders(self, surface_model):
        if 'Borders' in surface_model and surface_model['Borders'] is not None:
            for border in surface_model['Borders']['KeyValueOfguidanyType']:
                self.borders.append(MTMBorder(border))

    def get_mtmt(self) -> MTMT:
        return self.mtmt
