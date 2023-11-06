from slp_base import MultipleMappingFileValidator
from slp_base.slp_base.schema import Schema


class DrawioMappingFileValidator(MultipleMappingFileValidator):
    schema_filename = 'drawio_mapping_schema.json'

    def __init__(self, mappings_data: [bytes]):
        super(DrawioMappingFileValidator, self).__init__(
            Schema.from_package('slp_drawio', self.schema_filename), mappings_data)
