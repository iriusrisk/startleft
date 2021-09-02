import logging
logger = logging.getLogger(__name__)

class ThreatModel:
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
            "project": {
                "name": self.name,
                "id": self.id
            },
            "representations": [
                {
                    "name": self.representation,
                    "id": self.representation,
                    "type": "code"
                }
            ],
            "trustzones": [],
            "components": [],
            "dataflows": []
        }

        for trustzone in self.trustzones:
            data["trustzones"].append(trustzone.json())
        for component in self.components:
            data["components"].append(component.json())
        for dataflow in self.dataflows:
            data["dataflows"].append(dataflow.json())

        return data

    def add_trustzone(self, id=None, name=None, type=None, source=None, properties=None):
        self.trustzones.append(Trustzone(id=id, name=name, type=type, source=source, properties=properties))

    def add_component(self, id=None, name=None, type=None, parent=None, source=None, properties=None, tags=[]):
        self.components.append(Component(id=id, name=name, type=type, parent=parent, source=source, properties=properties, tags=tags))

    def add_dataflow(self, id=None, name=None, type=None, from_node=None, to_node=None, source=None, properties=None):
        self.dataflows.append(Dataflow(id=id, name=name, type=type, from_node=from_node, to_node=to_node, source=source, properties=properties))


class Trustzone:
    def __init__(self, id=None, name=None, type=None, source=None, properties=None):
        self.id = id
        self.name = name
        self.type = type
        self.source = source
        self.properties = properties

    def json(self):
        result = {
            "id": self.id,
            "name": self.name,
            "type": self.type
        }
        if self.properties:
            result["properties"] = self.properties
        return result


class Component:
    def __init__(self, id=None, name=None, type=None, parent=None, source=None, properties=None, tags=[]):
        self.id = id
        self.name = name
        self.type = type
        self.parent = parent
        self.source = source
        self.properties = properties
        self.tags = tags

    def json(self):
        result = {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "parent": self.parent,
            "tags": self.tags
        }
        if self.properties:
            result["properties"] = self.properties
        return result


class Dataflow:
    def __init__(self, id=None, name=None, type=None, from_node=None, to_node=None, source=None, properties=None):
        self.id = id
        self.name = name
        self.type = type
        self.from_node = from_node
        self.to_node = to_node
        self.source = source
        self.properties = properties

    def json(self):
        result = {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "from": self.from_node,
            "to":   self.to_node
        }
        if self.properties:
            result["properties"] = self.properties
        return result
