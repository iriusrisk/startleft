class Mitigation:
    def __init__(self, mitigation_id, name, description=None):
        self.id = mitigation_id
        self.name = name
        self.description = description
        self.risk_reduction = 100

    def __eq__(self, other):
        return other is not None and type(other) is Mitigation and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def json(self):
        json = {
            "name": self.name,
            "id": self.id,
            "riskReduction": self.risk_reduction
        }

        if self.description:
            json["description"] = self.description

        return json


class MitigationInstance:
    def __init__(self, mitigation_id, state):
        self.mitigation_id = mitigation_id
        self.state = state

    def __eq__(self, other):
        return other is not None and type(other) is MitigationInstance and self.mitigation_id == other.mitigation_id

    def __hash__(self):
        return hash(self.mitigation_id)

    def json(self):
        json = {
            "mitigation": self.mitigation_id,
            "state": self.state
        }

        return json
