from otm.otm.entity.representation import RepresentationType
from otm.otm.provider import Provider

application_json = 'application/json'
text_plain = 'text/plain'
application_octet_stream = 'application/octet-stream'
application_xml = 'application/xml'


class IacType(str, Provider):
    CLOUDFORMATION = ("CLOUDFORMATION", "CloudFormation", RepresentationType.CODE,
                      [application_json, 'text/yaml', text_plain, application_octet_stream])
    TERRAFORM = ("TERRAFORM", "Terraform", RepresentationType.CODE,
                 [text_plain, application_octet_stream, application_json])
    TFPLAN = ("TFPLAN", "Terraform Plan", RepresentationType.CODE,
              [text_plain, application_json, 'application/msword', 'text/vnd.graphviz', application_octet_stream])


class DiagramType(str, Provider):
    VISIO = ("VISIO", "Visio", RepresentationType.DIAGRAM,
             ['application/vnd.ms-visio.drawing.main+xml', application_octet_stream])
    LUCID = ("LUCID", "Lucidchart", RepresentationType.DIAGRAM,
             ['application/vnd.ms-visio.drawing.main+xml', application_octet_stream, 'application/zip'])
    DRAWIO = ("DRAWIO", "Drawio", RepresentationType.DIAGRAM,
              [application_octet_stream, application_xml, text_plain])


class EtmType(str, Provider):

    MTMT = ("MTMT", "Microsoft Threat Modeling Tool", RepresentationType.THREAT_MODEL,
            [application_octet_stream, application_xml, text_plain])
