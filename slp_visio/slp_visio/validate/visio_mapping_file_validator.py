from slp_base import MultipleMappingFileValidator
from slp_base.slp_base.schema import Schema


class VisioMappingFileValidator(MultipleMappingFileValidator):
    schema_filename = 'diagram_mapping_schema.json'

    def __init__(self, mappings_data: [bytes]):
        super(VisioMappingFileValidator, self).__init__(
            Schema.from_package('slp_visio', self.schema_filename), mappings_data)
