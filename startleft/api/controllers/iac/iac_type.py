from enum import Enum

from startleft.config import paths


class IacType(str, Enum):
    CLOUDFORMATION = ("CLOUDFORMATION", paths.default_cf_mapping_file)
    TERRAFORM = ("TERRAFORM", paths.default_tf_aws_mapping_file)

    def __new__(cls, value, def_map_file):
        obj = str.__new__(cls, [value])
        obj._value_ = value
        obj.def_map_file = def_map_file

        return obj
