from startleft import paths
from startleft.provider import Provider


class IacType(str, Provider):
    CLOUDFORMATION = ("CLOUDFORMATION", "CloudFormation", paths.default_cf_mapping_file, "code")
    TERRAFORM = ("TERRAFORM", "Terraform", paths.default_tf_mapping_file, "code")

