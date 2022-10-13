from otm.otm.otm import OTM, Component, Dataflow, Trustzone
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

    def add_default_trustzone(self, default_trustzone: Trustzone):
        self.add_trustzones([default_trustzone])
        return self

    def add_trustzones(self, trustzones: [Trustzone]):
        self.otm.trustzones = IterationUtils.remove_duplicates(self.otm.trustzones + trustzones)
        return self

    def add_components(self, components: [Component]):
        self.otm.components = components
        return self

    def add_dataflows(self, dataflows: [Dataflow]):
        self.otm.dataflows = dataflows
        return self

    def __init_otm(self):
        self.otm = OTM(self.project_name, self.project_id, self.provider)

