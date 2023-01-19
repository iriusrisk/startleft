from slp_base.slp_base import MultipleMappingFileValidator
from slp_base.slp_base.schema import Schema


class CloudformationMappingFileValidator(MultipleMappingFileValidator):
    schema_filename = 'iac_cft_mapping_schema.json'

    def __init__(self, mapping_files: [bytes]):
        super(CloudformationMappingFileValidator, self).__init__(
            Schema.from_package('slp_cft', self.schema_filename), mapping_files)
