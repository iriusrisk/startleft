import logging

from startleft.api.errors import MappingFileSchemaNotValidError
from startleft.validators.schema import Schema

logger = logging.getLogger(__name__)


class MappingValidator:
    def __init__(self, mapping_schema):
        self.mapping_schema = mapping_schema

    def validate(self, mapping_file):
        logger.debug("Validating mapping files")
        schema: Schema = Schema(self.mapping_schema)
        schema.validate(mapping_file)
        if not schema.valid:
            logger.error('Mapping files are not valid')
            logger.error(f"--- Schema errors---\n{schema.errors}\n--- End of schema errors ---")
            raise MappingFileSchemaNotValidError(schema.errors)
        logger.info("Mapping files are valid")
