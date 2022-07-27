import logging

from startleft.api.errors import MappingFileNotValidError
from startleft.processors.base.mapping_validator import MappingValidator
from startleft.validators.schema import Schema

logger = logging.getLogger(__name__)

MAX_SIZE = 5 * 1024 * 1024
MIN_SIZE = 5


class MappingFileValidator(MappingValidator):

    def __init__(self, schema, source):
        self.schema = schema
        self.source = source

    def validate(self):
        logger.debug('Validating mapping files')
        raise NotImplementedError

    def __validate_schema(self):
        schema: Schema = Schema(self.mapping_schema)
        schema.validate(self.source)
        if not schema.valid:
            logger.error('Mapping files are not valid')
            logger.error(f'--- Schema errors---\n{schema.errors}\n--- End of schema errors ---')
            raise MappingFileNotValidError('Mapping files are not valid',
                                           'Mapping file does not comply with the schema', str(schema.errors))
        logger.info('Mapping files are valid')
