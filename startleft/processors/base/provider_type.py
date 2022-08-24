from startleft.provider import Provider


class EtmType(str, Provider):
    MTMT = ("MTMT", "Microsoft Threat Modeling Tool", "threat-model")
