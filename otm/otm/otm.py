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

        if provider.provider_type == RepresentationType.DIAGRAM.value:
            default_size = {"width": 1000, "height": 1000}
            self.add_diagram_representation(id_=provider.provider_name, name=provider.provider_name,
                                            type_=provider.provider_type, size=default_size)
        else:
            self.add_representation(id_=provider.provider_name, name=provider.provider_name,
                                    type_=provider.provider_type)

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

    def add_trustzone(self, id=None, name=None, type=None, source=None, properties=None):
        self.trustzones.append(Trustzone(id=id, name=name, type=type, source=source, properties=properties))

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

    def add_representation(self, id_=None, name=None, type_=None):
        self.representations.append(Representation(id_=id_, name=name, type_=type_))

    def add_diagram_representation(self, id_=None, name=None, type_=None, size=None):
        self.representations.append(DiagramRepresentation(id_=id_, name=name, type_=type_, size=size))


class Trustzone:
    def __init__(self, id=None, name=None, type=None, source=None, properties=None, representations=None):
        self.id = id
        self.name = name
        self.type = type
        self.source = source
        self.properties = properties
        self.representations = representations

    def __eq__(self, other):
        return type(other) == Trustzone and self.id == other.id

    def __repr__(self) -> str:
        return f'Trustzone(id="{self.id}", name="{self.name}", type="{self.type}", source="{self.source}",' \
               f' properties="{self.properties}")'

    def __hash__(self):
        return hash(self.__repr__())

    def json(self):
        result = {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "risk": {
                "trustRating": 10
            }
        }
        if self.properties:
            result["properties"] = self.properties
        if self.representations:
            result["representations"] = [r.json()for r in self.representations]
        return result


class Component:
    def __init__(self, id=None, name=None, type=None, parent=None, parent_type=None, source=None,
                 properties=None, tags=None, representations=None):
        self.id = id
        self.name = name
        self.type = type
        self.parent = parent
        self.parent_type: str = parent_type
        self.source = source
        self.properties = properties
        self.tags = tags
        self.representations = representations

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
        if self.representations:
            result["representations"] = [r.json() for r in self.representations]
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
    THREAT_MODEL = 'threat-model'


class Representation:
    """
    See https://github.com/iriusrisk/OpenThreatModel#representations-object
    """

    def __init__(self, id_: str, name: str, type_: str, description: str = None, attributes: dict = None):
        self.id = id_
        self.name = name
        self.type = type_
        self.description = description
        self.attributes = attributes

    def json(self):
        result = {"name": self.name,
                  "id": self.id,
                  "type": self.type
                  }
        if self.description is not None:
            result['description'] = self.description
        if self.attributes is not None and len(self.attributes) > 0:
            result['attributes'] = self.attributes
        return result


class DiagramRepresentation(Representation):
    """
    See https://github.com/iriusrisk/OpenThreatModel#diagram
    """

    def __init__(self, id_: str, name: str, type_: str, description: str = None, attributes: dict = None, size=None):
        super(DiagramRepresentation, self).__init__(id_=id_, type_=type_, name=name, description=description,
                                                    attributes=attributes)
        self.size = size if self.type == RepresentationType.DIAGRAM.value else None

    def json(self):
        result = Representation.json(self)
        if self.size is not None:
            result['size'] = self.size
        return result


class RepresentationElement:
    """
    See https://github.com/iriusrisk/OpenThreatModel#representation-element-for-diagram
    """

    def __init__(self, id_: str, name: str, representation: str, position: dict = None, size: dict = None,
                 attributes: dict = None):
        self.id = id_
        self.name = name
        self.representation = representation
        self.position = position
        self.size = size
        self.attributes = attributes

    def json(self):
        result = {"name": self.name, "id": self.id}
        if self.representation is not None:
            result['representation'] = self.representation
        if self.size is not None and len(self.size) > 0:
            result['size'] = self.size
        if self.position is not None and len(self.position) > 0:
            result['position'] = self.position
        if self.attributes is not None and len(self.attributes) > 0:
            result['attributes'] = self.attributes

        return result
