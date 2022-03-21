from enum import Enum


class FileType(str, Enum):
    JSON = 'JSON'
    YAML = 'YAML'
    XML = 'XML'
