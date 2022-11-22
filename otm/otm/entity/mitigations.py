class OtmMitigation:
    def __init__(self, mitigation_id, name, description=None):
        self.id = mitigation_id
        self.name = name
        self.risk_reduction = 100
        self.description = description

    def __eq__(self, other):
        return other is not None and type(other) is OtmMitigation and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def json(self):
        result = {
            "name": self.name,
            "id": self.id,
            "riskReduction": self.risk_reduction
        }

        if self.description:
            result["description"] = self.description

        return result


class OtmMitigationInstance:
    def __init__(self, mitigation_id, state):
        self.mitigation_id = mitigation_id
        self.state = state

    def __eq__(self, other):
        return other is not None and type(other) is OtmMitigationInstance and self.mitigation_id == other.mitigation_id

    def __hash__(self):
        return hash(self.mitigation_id)

    def json(self):
        result = {
            "mitigation": self.mitigation_id,
            "state": self.state
        }

        return result
