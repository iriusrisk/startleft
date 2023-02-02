from slp_base import MultipleMappingFileValidator
from slp_base.slp_base.schema import Schema


class MTMTMappingFileValidator(MultipleMappingFileValidator):
    schema_filename = 'etm_mapping_schema.json'

    def __init__(self, mapping_files: [bytes]):
        super(MTMTMappingFileValidator, self).__init__(
            Schema.from_package('slp_mtmt', self.schema_filename), mapping_files)
