from otm.otm.entity.component import Component
from otm.otm.entity.dataflow import Dataflow
from otm.otm.entity.representation import Representation, DiagramRepresentation, RepresentationType
from otm.otm.entity.trustzone import Trustzone

REPRESENTATIONS_SIZE_DEFAULT_HEIGHT = 1000
REPRESENTATIONS_SIZE_DEFAULT_WIDTH = 1000


class OTM:
    def __init__(self, project_name, project_id, provider):
        self.project_name = project_name
        self.project_id = project_id
        self.representations = []
        self.trustzones = []
        self.components = []
        self.dataflows = []
        self.threats = []
        self.mitigations = []
        self.version = "0.1.0"
        self.__provider = provider

        self.add_default_representation()

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
            "representations": [],
            "trustZones": [],
            "components": [],
            "dataflows": []
        }

        for representation in self.representations:
            json["representations"].append(representation.json())
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

    def add_trustzone(self, id=None, name=None, type=None, source=None, properties=None):
        self.trustzones.append(
            Trustzone(trustzone_id=id, name=name, type=type, source=source, properties=properties))

    def add_component(self, id, name, type, parent, parent_type, source=None,
                      properties=None, tags=None):
        self.components.append(
            Component(component_id=id, name=name, component_type=type, parent=parent, parent_type=parent_type,
                      source=source, properties=properties, tags=tags))

    def add_dataflow(self, id, name, source_node, destination_node, bidirectional=None,
                     source=None, properties=None, tags=None):
        self.dataflows.append(Dataflow(dataflow_id=id, name=name, bidirectional=bidirectional, source_node=source_node,
                                       destination_node=destination_node, source=source, properties=properties,
                                       tags=tags))

    def add_representation(self, id_=None, name=None, type_=None):
        self.representations.append(Representation(id_=id_, name=name, type_=type_))

    def add_diagram_representation(self, id_=None, name=None, type_=None, size=None):
        self.representations.append(DiagramRepresentation(id_=id_, name=name, type_=type_, size=size))

    def add_default_representation(self):
        if not self.__provider.provider_type == RepresentationType.DIAGRAM.value:
            self.add_representation(id_=self.__provider.provider_name,
                                    name=self.__provider.provider_name,
                                    type_=self.__provider.provider_type)
        elif not self.representations:
            default_size = {"width": REPRESENTATIONS_SIZE_DEFAULT_WIDTH, "height": REPRESENTATIONS_SIZE_DEFAULT_HEIGHT}
            self.add_diagram_representation(id_=self.__provider.provider_name,
                                            name=self.__provider.provider_name,
                                            type_=self.__provider.provider_type,
                                            size=default_size)
