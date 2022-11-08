import logging
from enum import Enum

logger = logging.getLogger(__name__)


class OTM:
    def __init__(self, project_name, project_id, provider):
        self.project_name = project_name
        self.project_id = project_id

        self.representations = []
        self.trustzones = []
        self.components = []
        self.dataflows = []

        default_size = {"width": 1000, "height": 1000}
        self.representations.append(Representation(id_=provider.provider_name, name=provider.provider_name,
                                                   type_=provider.provider_type, size=default_size))

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
                "name": self.project_name,
                "id": self.project_id
            },
            "representations": [],
            "trustZones": [],
            "components": [],
            "dataflows": []
        }

        for representation in self.representations:
            data["representations"].append(representation.json())
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
                      properties=None, tags=None):
        self.components.append(
            Component(id=id, name=name, type=type, parent=parent, parent_type=parent_type,
                      source=source, properties=properties, tags=tags))

    def add_dataflow(self, id=None, name=None, bidirectional=None, source_node=None, destination_node=None,
                     source=None, properties=None, tags=None):
        self.dataflows.append(Dataflow(id=id, name=name, bidirectional=bidirectional, source_node=source_node,
                                       destination_node=destination_node, source=source, properties=properties,
                                       tags=tags))


class Trustzone:
    def __init__(self, id=None, name=None, source=None, properties=None):
        self.id = id
        self.name = name
        self.source = source
        self.properties = properties

    def __eq__(self, other):
        return type(other) == Trustzone and self.id == other.id

    def __repr__(self) -> str:
        return f'Trustzone(id="{self.id}", name="{self.name}", source="{self.source}", properties="{self.properties}")'

    def __hash__(self):
        return hash(self.__repr__())

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
                 properties=None, tags=None):
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
            }
        }

        if self.properties:
            result["properties"] = self.properties
        if self.tags:
            result["tags"] = self.tags
        return result


class Dataflow:
    def __init__(self, id=None, name=None, bidirectional=None, source_node=None, destination_node=None, source=None,
                 properties=None, tags=None):
        self.id = id
        self.name = name
        self.bidirectional = bidirectional
        self.source_node = source_node
        self.destination_node = destination_node
        self.source = source
        self.properties = properties
        self.tags = tags

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
        if self.tags:
            result["tags"] = self.tags
        return result


class RepresentationType(Enum):
    DIAGRAM = 'diagram'
    CODE = 'code'


class Representation:
    def __init__(self, id_: str, name: str, type_: str, description: str = None, attributes: dict = None, size=None):
        self.id = id_
        self.name = name
        self.type = type_
        self.description = description
        self.attributes = attributes
        self.size = size if self.type == RepresentationType.DIAGRAM.value else None

    def json(self):
        result = {"name": self.name,
                  "id": self.id,
                  "type": self.type
                  }
        if self.description is not None:
            result['description'] = self.description
        if self.attributes is not None and len(self.attributes) > 0:
            result['attributes'] = self.attributes
        if self.size is not None and len(self.size) > 0:
            result['size'] = self.size
        return result
