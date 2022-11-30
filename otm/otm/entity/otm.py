from otm.otm.entity.component import OtmComponent
from otm.otm.entity.dataflow import OtmDataflow
from otm.otm.entity.trustzone import OtmTrustzone


class Otm:
    def __init__(self, project_name, project_id, provider):
        self.project_name = project_name
        self.project_id = project_id
        self.representations_id = provider.provider_name
        self.representations_name = provider.provider_name
        self.representations_type = provider.provider_type
        self.trustzones = []
        self.components = []
        self.dataflows = []
        self.threats = []
        self.mitigations = []
        self.version = "0.1.0"
        self.representations_size_height = 1000
        self.representations_size_width = 1000

    def objects_by_type(self, type):
        if type == "trustzone":
            return self.trustzones
        if type == "component":
            return self.components
        if type == "dataflow":
            return self.dataflows

    def json(self):
        json = {
            "otmVersion": self.version,
            "project": {
                "name": self.project_name,
                "id": self.project_id
            },
            "representations": [
                {
                    "name": self.representations_name,
                    "id": self.representations_id,
                    "type": self.representations_type,
                }
            ],
            "trustZones": [],
            "components": [],
            "dataflows": []
        }

        if self.representations_type == "diagram":
            json["representations"][0]["size"] = {
                "width": self.representations_size_width,
                "height": self.representations_size_height
            }
        for trustzone in self.trustzones:
            json["trustZones"].append(trustzone.json())
        for component in self.components:
            json["components"].append(component.json())
        for dataflow in self.dataflows:
            json["dataflows"].append(dataflow.json())
        if len(self.threats) > 0:
            json["threats"] = []
            for threat in self.threats:
                json["threats"].append(threat.json())
        if len(self.mitigations) > 0:
            json["mitigations"] = []
            for mitigation in self.mitigations:
                json["mitigations"].append(mitigation.json())

        return json

    def add_trustzone(self, id, name, source=None, properties=None):
        self.trustzones.append(OtmTrustzone(trustzone_id=id, name=name, source=source, properties=properties))

    def add_component(self, id, name, type, parent, parent_type, source=None,
                      properties=None, tags=None):
        self.components.append(
            OtmComponent(component_id=id, name=name, component_type=type, parent=parent, parent_type=parent_type,
                         source=source, properties=properties, tags=tags))

    def add_dataflow(self, id, name, source_node, destination_node, bidirectional=None,
                     source=None, properties=None, tags=None):
        self.dataflows.append(OtmDataflow(dataflow_id=id, name=name, bidirectional=bidirectional, source_node=source_node,
                                          destination_node=destination_node, source=source, properties=properties,
                                          tags=tags))
