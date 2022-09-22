from slp_base.slp_base import MultipleMappingFileValidator


class TerraformMappingFileValidator(MultipleMappingFileValidator):
    schema = 'iac_mapping_schema.json'

    def __init__(self, mapping_files: [bytes]):
        super(TerraformMappingFileValidator, self).__init__(self.schema, mapping_files)
