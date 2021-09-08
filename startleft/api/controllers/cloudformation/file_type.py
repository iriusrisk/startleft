from enum import Enum


class FileType(str, Enum):
    JSON = 'JSON'
    YAML = 'YAML'
    CloudFormation = 'CloudFormation'
    HCL2 = 'HCL2'
    Terraform = 'Terraform'
    XML = 'XML'
