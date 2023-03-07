from otm.otm.entity.component import Component
from otm.otm.entity.dataflow import Dataflow
from otm.otm.entity.mitigation import Mitigation
from otm.otm.entity.otm import OTM
from otm.otm.entity.representation import Representation
from otm.otm.entity.threat import Threat
from otm.otm.entity.trustzone import Trustzone
from otm.otm.provider import Provider
from sl_util.sl_util.iterations_utils import remove_duplicates


class OTMBuilder:

    def __init__(self, project_id: str, project_name: str, provider: Provider):
        self.project_id = project_id
        self.project_name = project_name
        self.provider = provider

        self.__init_otm()

    def build(self):
        return self.otm

    def add_default_trustzone(self, default_trustzone: Trustzone):
        self.add_trustzones([default_trustzone])
        return self

    def add_trustzones(self, trustzones: [Trustzone]):
        self.otm.trustzones = remove_duplicates(self.otm.trustzones + trustzones)
        return self

    def add_components(self, components: [Component]):
        self.otm.components = components
        return self

    def add_dataflows(self, dataflows: [Dataflow]):
        self.otm.dataflows = dataflows
        return self

    def add_representations(self, representations: [Representation], extend: bool = True):
        if extend:
            self.otm.representations.extend(representations)
        else:
            self.otm.representations = representations

        return self

    def add_threats(self, threats: [Threat]):
        self.otm.threats = threats
        return self

    def add_mitigations(self, mitigations: [Mitigation]):
        self.otm.mitigations = mitigations
        return self

    def __init_otm(self):
        self.otm = OTM(self.project_name, self.project_id, self.provider)
