import logging

logger = logging.getLogger(__name__)


class OTM:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.representation = "CloudFormation"

        self.trustzones = []
        self.components = []
        self.dataflows = []

    def objects_by_type(self, type):
        if type == "trustzone":
            return self.trustzones
        if type == "component":
            return self.components
        if type == "dataflow":
            return self.dataflows

    def json(self):
        data = {
            "otmVersion": "0.1.0",
            "project": {
                "name": self.name,
                "id": self.id
            },
            "representations": [
                {
                    "name": self.representation,
                    "id": self.representation,
                    "type": "code",
                    "repository": {
                        "url": "http://mockedurl"
                    }
                }
            ],
            "trustZones": [],
            "components": [],
            "dataflows": []
        }

        for trustzone in self.trustzones:
            data["trustZones"].append(trustzone.json())
        for component in self.components:
            data["components"].append(component.json())
        for dataflow in self.dataflows:
            data["dataflows"].append(dataflow.json())

        return data

    def add_trustzone(self, id=None, name=None, source=None, properties=None):
        self.trustzones.append(Trustzone(id=id, name=name, source=source, properties=properties))

    def add_component(self, id=None, name=None, type=None, parent=None, parent_type=None, source=None,
                      properties=None, tags=[]):
        self.components.append(
            Component(id=id, name=name, type=type, parent=parent, parent_type=parent_type,
                      source=source, properties=properties, tags=tags))

    def add_dataflow(self, id=None, name=None, bidirectional=None, source_node=None, destination_node=None, source=None, properties=None):
        self.dataflows.append(Dataflow(id=id, name=name, bidirectional=bidirectional, source_node=source_node,
                                       destination_node=destination_node, source=source, properties=properties))


class Trustzone:
    def __init__(self, id=None, name=None, source=None, properties=None):
        self.id = id
        self.name = name
        self.source = source
        self.properties = properties

    def json(self):
        result = {
            "id": self.id,
            "name": self.name,
            "risk": {
                "trustRating": 10
            }
        }
        if self.properties:
            result["properties"] = self.properties
        return result


class Component:
    def __init__(self, id=None, name=None, type=None, parent=None, parent_type=None, source=None,
                 properties=None, tags=[]):
        self.id = id
        self.name = name
        self.type = type
        self.parent = parent
        self.parent_type: str = parent_type
        self.source = source
        self.properties = properties
        self.tags = tags

    def json(self):
        result = {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "parent": {
                self.parent_type: self.parent
            },
            "tags": self.tags
        }

        if self.properties:
            result["properties"] = self.properties
        return result


class Dataflow:
    def __init__(self, id=None, name=None, bidirectional=None, source_node=None, destination_node=None, source=None, properties=None):
        self.id = id
        self.name = name
        self.bidirectional = bidirectional
        self.source_node = source_node
        self.destination_node = destination_node
        self.source = source
        self.properties = properties

    def json(self):
        result = {
            "id": self.id,
            "name": self.name,
            "source": self.source_node,
            "destination": self.destination_node
        }
        if self.bidirectional is not None:
            result["bidirectional"] = self.bidirectional
        if self.properties:
            result["properties"] = self.properties
        return result
