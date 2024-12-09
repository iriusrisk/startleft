from sl_util.sl_util.str_utils import truncate

MAX_ID_SIZE = 255
MAX_NAME_SIZE = 255
MAX_TAG_SIZE = 255

class Dataflow:
    def __init__(self, dataflow_id, name, source_node, destination_node, bidirectional: bool = None,
                 source=None, attributes=None, tags=None):
        self.id = dataflow_id
        self.name = name
        self.bidirectional = bidirectional
        self.source_node = source_node
        self.destination_node = destination_node
        self.source = source
        self.attributes = attributes
        self.tags = tags

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

    def json(self):
        json = {
            "id": self.id,
            "name": self.name,
            "source": self.source_node,
            "destination": self.destination_node
        }

        if self.bidirectional is not None:
            json["bidirectional"] = self.bidirectional
        if self.attributes:
            json["attributes"] = self.attributes
        if self.tags:
            json["tags"] = self.tags

        return json

    def __repr__(self):
        return f'Dataflow(id="{self.id}", name="{self.name}", source="{self.source_node}", ' \
               f'destination="{self.destination_node}")'

    def __eq__(self, other):
        if other is None:
            return False

        if other is self:
            return True

        if not isinstance(other, Dataflow):
            return False

        return self.id == other.id
