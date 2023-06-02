import json
import logging
import os

import jsonschema
import pkg_resources

logger = logging.getLogger(__name__)


class Schema:
    def __init__(self, schema_path: str):
        self.schema_file = self.__load_schema(schema_path)
        logger.debug("Schema file loaded successfully")
        self.errors = ""
        self.valid = None

    def validate(self, document):
        try:
            jsonschema.validate(document, self.schema_file)
            self.valid = True
        except jsonschema.SchemaError as e:
            self.errors = e.message
            self.valid = False
        except jsonschema.ValidationError as e:
            self.errors = e.message
            self.valid = False

    def json(self):
        return json.dumps(self.schema_file, indent=2)

    def __load_schema(self, schema_path):
        logger.info(f"Loading schema file '{schema_path}'")
        with open(schema_path, "r") as f:
            return json.load(f)

    @staticmethod
    def from_package(package: str, filename: str):
        schema_path = pkg_resources.resource_filename(package, os.path.join('resources/schemas', filename))
        return Schema(schema_path)
