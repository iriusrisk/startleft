from startleft.processors.base.mapping import MultipleMappingFileValidator


class CloudformationMappingFileValidator(MultipleMappingFileValidator):
    schema = 'iac_mapping_schema.json'

    def __init__(self, mapping_files: [bytes]):
        super(CloudformationMappingFileValidator, self).__init__(self.schema, mapping_files)
