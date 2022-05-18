from startleft.iac.iac_type import IacType
from startleft.otm.otm import OTM, Component, Dataflow, Trustzone


class OtmBuilder:

    def __init__(self, project_id: str, project_name: str, provider: IacType):
        self.project_id = project_id
        self.project_name = project_name
        self.provider = provider

        self.__init_otm()

    def build(self):
        return self.otm

    def add_default_trustzone(self, default_trustzone: dict):
        self.otm.add_trustzone(default_trustzone['id'], default_trustzone['type'])
        return self

    def add_trustzones(self, trustzones: [Trustzone]):
        self.otm.trustzones = trustzones
        return self

    def add_components(self, components: [Component]):
        self.otm.components = components
        return self

    def add_dataflows(self, dataflows: [Dataflow]):
        self.otm.dataflows = dataflows
        return self

    def __init_otm(self):
        self.otm = OTM(self.project_name, self.project_id, self.provider)

