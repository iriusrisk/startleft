from startleft.provider import Provider


class EtmType(str, Provider):
    MTMT = ("MTMT", "Microsoft Threat Model", "etm")


class DiagramType(str, Provider):
    VISIO = ("VISIO", "Visio", "diagram")
