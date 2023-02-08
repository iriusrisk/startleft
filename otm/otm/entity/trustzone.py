class OtmTrustzone:
    def __init__(self, trustzone_id, name, source=None, type=type, attributes=None, representations=None):
        self.id = trustzone_id
        self.name = name
        self.type = type
        self.source = source
        self.attributes = attributes
        self.trustrating = 10
        self.representations = representations

    def __eq__(self, other):
        return type(other) == OtmTrustzone and self.id == other.id

    def __repr__(self) -> str:
        return f'Trustzone(id="{self.id}", name="{self.name}", type="{self.type}", source="{self.source}", ' \
               f'attributes="{self.attributes}, trustrating="{self.trustrating}")'

    def __hash__(self):
        return hash(self.__repr__())

    def json(self):
        json = {
            "id": self.id,
            "name": self.name,
            "risk": {
                "trustRating": self.trustrating
            }
        }

        if self.attributes:
            json["attributes"] = self.attributes
        if self.representations:
            json["representations"] = [r.json() for r in self.representations]

        return json
