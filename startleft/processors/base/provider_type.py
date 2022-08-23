from startleft.provider import Provider


class EtmType(str, Provider):
    MTMT = ("MTMT", "Microsoft Threat Model", "threat-model")
