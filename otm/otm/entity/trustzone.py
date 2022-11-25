class OtmTrustzone:
    def __init__(self, trustzone_id, name, source=None, properties=None):
        self.id = trustzone_id
        self.name = name
        self.source = source
        self.properties = properties
        self.trustrating = 10

    def __eq__(self, other):
        return type(other) == OtmTrustzone and self.id == other.id

    def __repr__(self) -> str:
        return f'Trustzone(id="{self.id}", name="{self.name}", source="{self.source}", properties="{self.properties}, trustrating="{self.trustrating}")'

    def __hash__(self):
        return hash(self.id)

    def json(self):
        json = {
            "id": self.id,
            "name": self.name,
            "risk": {
                "trustRating": self.trustrating
            }
        }

        if self.properties:
            json["properties"] = self.properties

        return json
