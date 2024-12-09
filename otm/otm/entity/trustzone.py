from otm.otm.entity.parent_type import ParentType
from sl_util.sl_util.str_utils import truncate

MAX_ID_SIZE = 255
MAX_NAME_SIZE = 255

class Trustzone:
    def __init__(self, trustzone_id, name, parent=None, parent_type: ParentType = None, source=None, type=type,
                 attributes=None, trustrating=10, representations=None):
        self.id = trustzone_id
        self.name = name
        self.type = type
        self.parent = parent
        self.parent_type: ParentType = parent_type
        self.source = source
        self.attributes = attributes
        self.trustrating = trustrating
        self.representations = representations

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = truncate(value, MAX_ID_SIZE)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = truncate(value, MAX_NAME_SIZE)

    def __eq__(self, other):
        return type(other) == Trustzone and self.id == other.id

    def __repr__(self) -> str:
        return f'Trustzone(id="{self.id}", name="{self.name}", type="{self.type}", source="{self.source}", ' \
               f'attributes="{self.attributes}, trustrating="{self.trustrating}")'

    def __hash__(self):
        return hash(self.__repr__())

    def json(self):
        json = {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "risk": {
                "trustRating": self.trustrating
            }
        }
        if self.parent and self.parent_type:
            json["parent"] = {
                str(self.parent_type): self.parent
            }
        if self.attributes:
            json["attributes"] = self.attributes
        if self.representations:
            json["representations"] = [r.json() for r in self.representations]

        return json
