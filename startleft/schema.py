import jsonschema
import json


class Schema:
    def __init__(self, schema):
        self.schema = schema
        self.errors = ""
        self.valid = None

    def validate(self, document):
        try:
            jsonschema.validate(document, self.schema)
            self.valid = True
        except jsonschema.SchemaError as e:
            self.errors = e
            self.valid = False
        except jsonschema.ValidationError as e:
            self.errors = e
            self.valid = False

    def json(self):
        return json.dumps(self.schema, indent=2)
