PROJECT_SUCCESSFULLY_CREATED = 'Provided CloudFormation Template has been successfully processed and a new IriusRisk ' \
                               'project has been created with the provided metadata'
PROJECT_SUCCESSFULLY_UPDATED = 'IriusRisk project has been updated with the latest changes from the CloudFormation ' \
                               'Template provided'
UNAUTHORIZED_EXCEPTION = 'Authentication information is missing, invalid or not granted to perform this action'
BAD_REQUEST = 'Bad request'
FORBIDDEN_OPERATION = 'Forbidden operation'
PROJECT_NOT_FOUND = 'Project not found'
UNEXPECTED_API_ERROR = 'Unexpected API error'
INCONSISTENT_IDS = 'Generated OTM file has inconsistent IDs'
OTM_SCHEMA_IS_NOT_VALID = 'OTM schema is not valid'
OTM_FILE_NOT_FOUND = 'Cannot find OTM file'
OTM_SUCCESSFULLY_CREATED = 'Provided IaC file has been successfully processed and a new OTM file ' \
                               'has been created'
MAPPING_FILE_NOT_FOUND = 'Cannot find mapping file'
MAPPING_FILE_SCHEMA_NOT_VALID = 'Mapping files are not valid'
ERROR_WRITING_THREAT_MODEL = 'Unable to create the threat model'

# CLI
IAC_FILE_NAME = 'iac-file'

IAC_TYPE_NAME = '--iac-type'
IAC_TYPE_SHORTNAME = '-t'
IAC_TYPE_DESC = 'The IaC file type.'
IAC_TYPE_SUPPORTED = ['CLOUDFORMATION', 'TERRAFORM']

MAPPING_FILE_NAME = '--mapping-file'
MAPPING_FILE_SHORTNAME = '-m'
MAPPING_FILE_DESC = 'Mapping file to parse the IaC file.'

OUTPUT_FILE_NAME = '--output-file'
OUTPUT_FILE_SHORTNAME = '-o'
OUTPUT_FILE_DESC = 'OTM output file.'
OUTPUT_FILE = 'threatmodel.otm'

PROJECT_NAME_NAME = '--project-name'
PROJECT_NAME_SHORTNAME = '-n'
PROJECT_NAME_DESC = 'Project name.'

PROJECT_ID_NAME = '--project-id'
PROJECT_ID_SHORTNAME = '-i'
PROJECT_ID_DESC = 'Project id.'

