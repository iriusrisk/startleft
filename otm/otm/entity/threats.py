from otm.otm.entity.mitigations import OtmMitigationInstance


class OtmThreat:
    def __init__(self, threat_id, name, category, description=None):
        self.id = threat_id
        self.name = name
        self.description = description
        self.category = category

    def __eq__(self, other):
        return other is not None and type(other) is OtmThreat and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def json(self):
        result = {
            "name": self.name,
            "id": self.id,
            "categories": [
                self.category
            ],
            "risk": {
                "likelihood": 100,
                "impact": 100
            }
        }

        if self.description:
            result["description"] = self.description

        return result


class OtmThreatInstance:
    def __init__(self, threat_id, state, mitigations: [OtmMitigationInstance] = None):
        self.threat_id = threat_id
        self.state = state
        self.mitigations = mitigations or []

    def __eq__(self, other):
        return other is not None and type(other) is OtmThreatInstance and self.threat_id == other.threat_id

    def __hash__(self):
        return hash(self.threat_id)

    def add_mitigation(self, mitigation: OtmMitigationInstance):
        self.mitigations.append(mitigation)

    def json(self):
        result = {
            "threat": self.threat_id,
            "state": self.state,
            "mitigations": []
        }

        if len(self.mitigations) > 0:
            for mitigation in self.mitigations:
                result["mitigations"].append(mitigation.json())

        return result
