class Dataflow:
    def __init__(self, dataflow_id, name, source_node, destination_node, bidirectional: bool = None,
                 source=None, properties=None, tags=None):
        self.id = dataflow_id
        self.name = name
        self.bidirectional = bidirectional
        self.source_node = source_node
        self.destination_node = destination_node
        self.source = source
        self.properties = properties
        self.tags = tags

    def json(self):
        json = {
            "id": self.id,
            "name": self.name,
            "source": self.source_node,
            "destination": self.destination_node
        }

        if self.bidirectional is not None:
            json["bidirectional"] = self.bidirectional
        if self.properties:
            json["properties"] = self.properties
        if self.tags:
            json["tags"] = self.tags

        return json

    def __repr__(self):
        return f'Dataflow(id="{self.id}", name="{self.name}", source="{self.source_node}", ' \
               f'destination="{self.destination_node}")'

