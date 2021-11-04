import logging

from startleft.api.errors import MappingFileSchemaNotValidError
from startleft.validators.schema import Schema, MappingSchema

logger = logging.getLogger(__name__)


class MappingValidator:

    def validate(self, mapping):
        logger.debug("Validating mapping schema")
        schema: Schema = MappingSchema()
        logger.debug(f"--- Schema to validate against ---\n{schema.json()}\n--- End of schema ---")
        schema.validate(mapping)
        if not schema.valid:
            logger.error('Mapping files are not valid')
            logger.error(f"--- Schema errors---\n{schema.errors}\n--- End of schema errors ---")
            raise MappingFileSchemaNotValidError(schema.errors)
