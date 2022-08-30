from startleft.processors.base.mapping import MultipleMappingFileValidator


class VisioMappingFileValidator(MultipleMappingFileValidator):
    schema = 'diagram_mapping_schema.json'

    def __init__(self, mappings_data: [bytes]):
        super(VisioMappingFileValidator, self).__init__(self.schema, mappings_data)
