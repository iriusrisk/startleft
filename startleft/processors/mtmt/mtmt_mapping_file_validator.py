from startleft.paths import etm_mapping_schema
from startleft.processors.base.mapping import MultipleMappingFileValidator


class MTMTMappingFileValidator(MultipleMappingFileValidator):
    schema = 'etm_mapping_schema.json'

    def __init__(self, mapping_files: [bytes]):
        super(MTMTMappingFileValidator, self).__init__(self.schema, mapping_files)
