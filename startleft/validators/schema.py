import json
import logging
import os

import jsonschema
import pkg_resources
import yaml

logger = logging.getLogger(__name__)


class Schema:
    def __init__(self, schema_file_name: str):
        self.schema = self.__load_schema(schema_file_name)
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

    def __load_schema(self, schema_file_name):
        schema_path = pkg_resources.resource_filename('startleft', os.path.join('data', schema_file_name))
        logger.debug(f"Loading schema from {schema_path}")
        with open(schema_path, "r") as f:
            return yaml.load(f, Loader=yaml.BaseLoader)


class OtmSchema(Schema):
    def __init__(self):
        Schema.__init__(self, 'otm_schema.json')


class MappingSchema(Schema):
    def __init__(self):
        Schema.__init__(self, 'mapping_schema.json')
