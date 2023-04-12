from slp_base.slp_base import MultipleMappingFileValidator
from slp_base.slp_base.schema import Schema


class TFPlanMappingFileValidator(MultipleMappingFileValidator):
    schema_filename = 'iac_tfplan_mapping_schema.json'

    def __init__(self, mapping_files: [bytes]):
        super(TFPlanMappingFileValidator, self).__init__(
            Schema.from_package('slp_tfplan', self.schema_filename), mapping_files)
