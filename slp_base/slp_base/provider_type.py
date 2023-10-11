from otm.otm.entity.representation import RepresentationType
from otm.otm.provider import Provider


class IacType(str, Provider):
    CLOUDFORMATION = ("CLOUDFORMATION", "CloudFormation", RepresentationType.CODE,
                      ['application/json', 'text/yaml', 'text/plain', 'application/octet-stream'])
    TERRAFORM = ("TERRAFORM", "Terraform", RepresentationType.CODE,
                 ['text/plain', 'application/octet-stream', 'application/json'])
    TFPLAN = ("TFPLAN", "Terraform Plan", RepresentationType.CODE,
              ['text/plain', 'application/json', 'application/msword', 'text/vnd.graphviz', 'application/octet-stream'])


class DiagramType(str, Provider):
    VISIO = ("VISIO", "Visio", RepresentationType.DIAGRAM,
             ['application/vnd.ms-visio.drawing.main+xml', 'application/octet-stream'])
    LUCID = ("LUCID", "Lucidchart", RepresentationType.DIAGRAM,
             ['application/vnd.ms-visio.drawing.main+xml', 'application/octet-stream', 'application/zip'])
    # DRAWIO = ("DRAWIO", "Drawio", RepresentationType.DIAGRAM,
    #           ['application/octet-stream', 'application/xml', 'text/plain'])


class EtmType(str, Provider):
    MTMT = ("MTMT", "Microsoft Threat Modeling Tool", RepresentationType.THREAT_MODEL,
            ['application/octet-stream', 'application/xml', 'text/plain'])
