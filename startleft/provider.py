from enum import Enum

from startleft.config import paths


class Provider(str, Enum):
    CLOUDFORMATION = ("CLOUDFORMATION", "CloudFormation", paths.default_cf_mapping_file, "code")
    TERRAFORM = ("TERRAFORM", "Terraform", paths.default_tf_aws_mapping_file, "code")
    VISIO = ("VISIO", "Visio", None, "diagram")

    def __new__(cls, value, provider_name: str = None, def_map_file: str = None, provider_type: str = None):
        obj = str.__new__(cls, [value])
        obj._value_ = value
        obj.provider_name = provider_name
        obj.def_map_file = def_map_file
        obj.provider_type = provider_type

        return obj

    @classmethod
    def allowed_providers(cls) -> [str]:
        allowed = []

        for provider in Provider:
            allowed.append(provider.name)

        return allowed
