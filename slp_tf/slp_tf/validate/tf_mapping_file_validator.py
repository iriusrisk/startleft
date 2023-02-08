from slp_base.slp_base import MultipleMappingFileValidator
from slp_base.slp_base.schema import Schema


class TerraformMappingFileValidator(MultipleMappingFileValidator):
    schema_filename = 'iac_tf_mapping_schema.json'

    def __init__(self, mapping_files: [bytes]):
        super(TerraformMappingFileValidator, self).__init__(
            Schema.from_package('slp_tf', self.schema_filename), mapping_files)
