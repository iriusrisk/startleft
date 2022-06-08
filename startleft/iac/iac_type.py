from startleft.provider import Provider


class IacType(str, Provider):
    CLOUDFORMATION = ("CLOUDFORMATION", "CloudFormation", "code")
    TERRAFORM = ("TERRAFORM", "Terraform", "code")
