from otm.otm.entity.representation import RepresentationType
from otm.otm.provider import Provider


class IacType(str, Provider):
    CLOUDFORMATION = ("CLOUDFORMATION", "CloudFormation", RepresentationType.CODE)
    TERRAFORM = ("TERRAFORM", "Terraform", RepresentationType.CODE)


class DiagramType(str, Provider):
    VISIO = ("VISIO", "Visio", RepresentationType.DIAGRAM)
    LUCID = ("LUCID", "Lucidchart", RepresentationType.DIAGRAM)


class EtmType(str, Provider):
    MTMT = ("MTMT", "Microsoft Threat Modeling Tool", RepresentationType.THREAT_MODEL)

