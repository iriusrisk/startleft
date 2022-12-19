from enum import Enum

from sl_util.sl_util.lang_utils import auto_repr, auto_str, auto_eq


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
        json = {
            "name": self.name,
            "id": self.id,
            "type": self.type
        }

        if self.description is not None:
            json['description'] = self.description
        if self.attributes is not None and len(self.attributes) > 0:
            json['attributes'] = self.attributes

        return json


class DiagramRepresentation(Representation):
    """
    See https://github.com/iriusrisk/OpenThreatModel#diagram
    """

    def __init__(self, id_: str, name: str, type_: str, description: str = None, attributes: dict = None, size=None):
        super(DiagramRepresentation, self).__init__(id_=id_, type_=type_, name=name, description=description,
                                                    attributes=attributes)
        self.size = size if self.type == RepresentationType.DIAGRAM.value else None

    def json(self):
        json = Representation.json(self)

        if self.size is not None:
            json['size'] = self.size

        return json


@auto_repr
@auto_str
@auto_eq
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
        json = {"name": self.name, "id": self.id}

        if self.representation is not None:
            json['representation'] = self.representation
        if self.size is not None and len(self.size) > 0:
            json['size'] = self.size
        if self.position is not None and len(self.position) > 0:
            json['position'] = self.position
        if self.attributes is not None and len(self.attributes) > 0:
            json['attributes'] = self.attributes

        return json
