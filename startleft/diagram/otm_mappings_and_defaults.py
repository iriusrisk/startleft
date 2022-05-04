from startleft.otm import Trustzone

OTM_DEFAULT_ID = 'visio-otm-id'
OTM_DEFAULT_NAME = 'visio-otm-name'

PUBLIC_CLOUD_TRUSTZONE = Trustzone(
    id='b61d6911-338d-46a8-9f39-8dcd24abfe91',
    name='Public Cloud'
)
PRIVATE_CLOUD_TRUSTZONE = Trustzone(
    id='2ab4effa-40b7-4cd2-ba81-8247d29a6f2d',
    name='Private Secured'
)
DEFAULT_TRUSTZONE = PUBLIC_CLOUD_TRUSTZONE
MAPPING_VISIO_OTM_TRUSTZONES = {
    'Public Cloud': PUBLIC_CLOUD_TRUSTZONE,
    'Private Secured Cloud': PRIVATE_CLOUD_TRUSTZONE
}

DEFAULT_COMPONENT_TYPE = 'empty-component'

MAPPING_VISIO_OTM_COMPONENTS = {
    'Amazon EC2': 'ec2',
    'Amazon CloudWatch': 'cloudwatch',
    'Database': 'rds'
}