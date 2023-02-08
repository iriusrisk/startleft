from otm.otm.provider import Provider


class IacType(str, Provider):
    CLOUDFORMATION = ("CLOUDFORMATION", "CloudFormation", "code")
    TERRAFORM = ("TERRAFORM", "Terraform", "code")


class DiagramType(str, Provider):
    VISIO = ("VISIO", "Visio", "diagram")
    LUCID = ("LUCID", "Lucidchart", "diagram")


class EtmType(str, Provider):
    MTMT = ("MTMT", "Microsoft Threat Modeling Tool", "threat-model")

