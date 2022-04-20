from enum import Enum

from startleft.config import paths


class IacType(str, Enum):
    CLOUDFORMATION = ("CLOUDFORMATION", "CloudFormation", paths.default_cf_mapping_file)
    TERRAFORM = ("TERRAFORM", "Terraform", paths.default_tf_aws_mapping_file)

    def __new__(cls, value, description: str = None, def_map_file=None):
        obj = str.__new__(cls, [value])
        obj._value_ = value
        obj.description = description
        obj.def_map_file = def_map_file

        return obj
