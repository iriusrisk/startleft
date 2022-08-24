import logging

from slp_base.slp_base.errors import MappingFileNotValidError
from slp_base.slp_base.schema import Schema

logger = logging.getLogger(__name__)

MAX_SIZE = 5 * 1024 * 1024
MIN_SIZE = 5


class GenericMappingValidator:
    """
    deprecated: Use MappingFileValidator instead
    """

    def __init__(self, mapping_schema):
        self.mapping_schema = mapping_schema

    def validate(self, mapping_file):
        logger.debug('Validating mapping files')
        self.__validate_schema(mapping_file)

    def __validate_schema(self, mapping_file):
        schema: Schema = Schema(self.mapping_schema)
        schema.validate(mapping_file)
        if not schema.valid:
            logger.error('Mapping files are not valid')
            logger.error(f'--- Schema errors---\n{schema.errors}\n--- End of schema errors ---')
            raise MappingFileNotValidError('Mapping files are not valid',
                                           'Mapping file does not comply with the schema', str(schema.errors))
        logger.info('Mapping files are valid')

    @staticmethod
    def check_data_size(mapping_data: bytes):
        """
        Validate the size of mapping data [bytes]
        """
        size = len(mapping_data)
        if type(mapping_data) == 'bytes' and size is None or size > MAX_SIZE or size < MIN_SIZE:
            msg = 'Mapping files are not valid. Invalid size'
            raise MappingFileNotValidError('Mapping files are not valid', msg, msg)
