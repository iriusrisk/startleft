from otm.otm.entity.representation import RepresentationType
from otm.otm.provider import Provider

application_json = 'application/json'
text_plain = 'text/plain'
text_xml = 'text/xml'
application_octet_stream = 'application/octet-stream'
application_xml = 'application/xml'
VALID_YAML_MIME_TYPES = [
    "text/yml",
    "text/yaml",
    "text/x-yml",
    "text/x-yaml",
    "application/yml",
    "application/yaml",
    "application/x-yml",
    "application/x-yaml"
]


class IacType(str, Provider):
    CLOUDFORMATION = ("CLOUDFORMATION", "CloudFormation", RepresentationType.CODE,
                      [application_json, text_plain, application_octet_stream] + VALID_YAML_MIME_TYPES)
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
              [application_octet_stream, application_xml, text_xml, text_plain])


class EtmType(str, Provider):
    MTMT = ("MTMT", "Microsoft Threat Modeling Tool", RepresentationType.THREAT_MODEL,
            [application_octet_stream, application_xml, text_plain])
