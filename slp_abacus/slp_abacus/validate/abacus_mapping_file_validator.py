import logging

from slp_base import MultipleMappingFileValidator
from slp_base.slp_base.schema import Schema

logger = logging.getLogger(__name__)

class AbacusMappingFileValidator(MultipleMappingFileValidator):
    # schema_filename = 'abacus_mapping_schema.json'

    def __init__(self, mappings_data: [bytes]):
        super(AbacusMappingFileValidator, self).__init__(None, None)

    def validate(self):
        logger.debug('Validating mapping files')


