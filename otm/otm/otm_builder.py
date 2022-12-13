from otm.otm.entity.otm import Otm
from otm.otm.entity.dataflow import OtmDataflow
from otm.otm.entity.component import OtmComponent
from otm.otm.entity.trustzone import OtmTrustzone
from otm.otm.entity.representation import Representation
from otm.otm.entity.mitigation import OtmMitigation
from otm.otm.entity.threat import OtmThreat
from otm.otm.provider import Provider
from sl_util.sl_util.iterations_utils import IterationUtils


class OtmBuilder:

    def __init__(self, project_id: str, project_name: str, provider: Provider):
        self.project_id = project_id
        self.project_name = project_name
        self.provider = provider

        self.__init_otm()

    def build(self):
        return self.otm

    def add_default_trustzone(self, default_trustzone: OtmTrustzone):
        self.add_trustzones([default_trustzone])
        return self

    def add_trustzones(self, trustzones: [OtmTrustzone]):
        self.otm.trustzones = IterationUtils.remove_duplicates(self.otm.trustzones + trustzones)
        return self

    def add_components(self, components: [OtmComponent]):
        self.otm.components = components
        return self

    def add_dataflows(self, dataflows: [OtmDataflow]):
        self.otm.dataflows = dataflows
        return self

    def add_representations(self, representations: [Representation]):
        self.otm.representations.extend(representations)
        return self

    def add_threats(self, threats: [OtmThreat]):
        self.otm.threats = threats
        return self

    def add_mitigations(self, mitigations: [OtmMitigation]):
        self.otm.mitigations = mitigations
        return self

    def __init_otm(self):
        self.otm = Otm(self.project_name, self.project_id, self.provider)
