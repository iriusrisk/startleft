import abc
import logging

from startleft.api.errors import MappingFileNotValidError
from startleft.validators.schema import Schema

logger = logging.getLogger(__name__)

MAX_SIZE = 5 * 1024 * 1024
MIN_SIZE = 5


class MappingLoader(metaclass=abc.ABCMeta):
    """
    Formal Interface to load the mapping data
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
                hasattr(subclass, 'load') and callable(subclass.load)
                or NotImplemented)

    @abc.abstractmethod
    def load(self):
        """Load mapping data"""
        raise NotImplementedError


class MappingValidator(metaclass=abc.ABCMeta):
    """
    Formal Interface to validate a mapping file
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
                hasattr(subclass, 'validate') and callable(subclass.validate)
                or NotImplemented)

    @abc.abstractmethod
    def validate(self):
        """Validate mapping file"""
        raise NotImplementedError


class MappingFileValidator(MappingValidator):
    def __init__(self, schema, mapping_file: bytes):
        self.schema = schema
        self.mapping_file = mapping_file

    def validate(self):
        logger.debug('Validating mapping file')
        validate_mapping_file(self.schema, self.mapping_file)


class MultipleMappingFileValidator(MappingValidator):
    def __init__(self, schema, mapping_files: [bytes]):
        self.schema = schema
        self.mapping_files = mapping_files

    def validate(self):
        logger.debug('Validating mapping files')
        for mapping_file in self.mapping_files:
            validate_mapping_file(self.schema, mapping_file)


def validate_size(mapping_file_data: bytes):
    size = len(mapping_file_data)

    if size is None or size > MAX_SIZE or size < MIN_SIZE:
        msg = 'Invalid size'
        raise MappingFileNotValidError('Mapping file is not valid', msg, msg)

    logger.info('Mapping file size is valid')


def validate_schema(schema: str, mapping_file: bytes):
    schema: Schema = Schema(schema)
    schema.validate(mapping_file)
    if not schema.valid:
        logger.error('Mapping file is not valid')
        logger.error(f'--- Schema errors ---\n{schema.errors}\n--- End of schema errors ---')
        raise MappingFileNotValidError('Mapping file is not valid',
                                       'Mapping file does not comply with the schema', str(schema.errors))
    logger.info('Mapping file schema is valid')


def validate_mapping_file(schema: str, mapping_file: bytes):
    validate_size(mapping_file)
    validate_schema(schema, mapping_file)
    logger.info('Mapping file is valid')
