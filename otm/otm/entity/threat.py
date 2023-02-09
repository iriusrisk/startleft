from otm.otm.entity.mitigation import MitigationInstance


class Threat:
    def __init__(self, threat_id, name, category, description=None):
        self.id = threat_id
        self.name = name
        self.category = category
        self.description = description
        self.likelihood = 100
        self.impact = 100

    def __eq__(self, other):
        return other is not None and type(other) is Threat and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def json(self):
        json = {
            "name": self.name,
            "id": self.id,
            "categories": [
                self.category
            ],
            "risk": {
                "likelihood": self.likelihood,
                "impact": self.impact
            }
        }

        if self.description:
            json["description"] = self.description

        return json


class ThreatInstance:
    def __init__(self, threat_id, state, mitigations: [MitigationInstance] = None):
        self.threat_id = threat_id
        self.state = state
        self.mitigations = mitigations or []

    def __eq__(self, other):
        return other is not None and type(other) is ThreatInstance and self.threat_id == other.threat_id

    def __hash__(self):
        return hash(self.threat_id)

    def add_mitigation(self, mitigation: MitigationInstance):
        self.mitigations.append(mitigation)

    def json(self):
        json = {
            "threat": self.threat_id,
            "state": self.state
        }

        if len(self.mitigations) > 0:
            json["mitigations"] = []
            for mitigation in self.mitigations:
                json["mitigations"].append(mitigation.json())

        return json
