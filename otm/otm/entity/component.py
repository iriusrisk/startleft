from otm.otm.entity.parent_type import ParentType
from otm.otm.entity.threat import ThreatInstance


class Component:
    def __init__(self, component_id, name, component_type, parent, parent_type: ParentType, source=None,
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
        self.representations = representations

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
