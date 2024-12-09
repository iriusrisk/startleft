from typing import List

from otm.otm.entity.parent_type import ParentType
from otm.otm.entity.representation import RepresentationElement
from otm.otm.entity.threat import ThreatInstance
from sl_util.sl_util.str_utils import truncate

MAX_ID_SIZE = 255
MAX_NAME_SIZE = 255
MAX_TAG_SIZE = 255

class Component:
    def __init__(self, component_id, name, component_type=None, parent=None, parent_type: ParentType = None, source=None,
                 attributes=None, tags=None, threats: [ThreatInstance] = None, representations=None):
        self.id = component_id
        self.name = name
        self.type = component_type
        self.parent = parent
        self.parent_type: ParentType = parent_type
        self.source = source
        self.attributes = attributes
        self.tags = tags
        self.threats: [ThreatInstance] = threats or []
        self.representations: List[RepresentationElement] = representations

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = truncate(value, MAX_NAME_SIZE)

    @property
    def tags (self):
        return self._tags

    @tags.setter
    def tags(self, value):
        self._tags = [tag for tag in value if tag and len(tag) <= MAX_TAG_SIZE] if value else None

    def add_threat(self, threat: ThreatInstance):
        self.threats.append(threat)

    def json(self):
        json = {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "parent": {
                str(self.parent_type): self.parent
            }
        }

        if self.attributes:
            json["attributes"] = self.attributes
        if self.tags:
            json["tags"] = self.tags
        if self.representations:
            json["representations"] = [r.json() for r in self.representations]

        if len(self.threats) > 0:
            json["threats"] = []
            for threat in self.threats:
                json["threats"].append(threat.json())

        return json
