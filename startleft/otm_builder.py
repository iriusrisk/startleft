from startleft.otm import OTM, Component, Dataflow, Trustzone
from startleft.provider import Provider


class OtmBuilder:

    def __init__(self, project_id: str, project_name: str, default_trustzone: dict):
        self.project_id = project_id
        self.project_name = project_name
        self.default_trustzone = default_trustzone

        self.__init_otm()

    def build(self):
        return self.otm

    def add_default_trustzone(self, default_trustzone: dict):
        self.default_trustzone = default_trustzone
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
        self.otm = OTM(self.project_name, self.project_id, Provider.VISIO)
        self.__add_default_trustzone()

    def __add_default_trustzone(self):
        self.otm.add_trustzone(self.default_trustzone['id'], self.default_trustzone['type'])
