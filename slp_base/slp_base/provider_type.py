from otm.otm.entity.representation import RepresentationType
from otm.otm.provider import Provider


class IacType(str, Provider):
    CLOUDFORMATION = ("CLOUDFORMATION", "CloudFormation", RepresentationType.CODE,
                      ['application/json', 'text/yaml', 'text/plain', 'application/octet-stream'])
    TERRAFORM = ("TERRAFORM", "Terraform", RepresentationType.CODE,
                 ['text/plain', 'application/octet-stream', 'application/json', 'application/msword',
                  'text/vnd.graphviz'])


class DiagramType(str, Provider):
    VISIO = ("VISIO", "Visio", RepresentationType.DIAGRAM,
             ['application/vnd.ms-visio.drawing.main+xml', 'application/octet-stream'])
    LUCID = ("LUCID", "Lucidchart", RepresentationType.DIAGRAM,
             ['application/vnd.ms-visio.drawing.main+xml', 'application/octet-stream', 'application/zip'])


class EtmType(str, Provider):
    MTMT = ("MTMT", "Microsoft Threat Modeling Tool", RepresentationType.THREAT_MODEL,
            ['application/octet-stream', 'application/xml', 'text/plain'])

