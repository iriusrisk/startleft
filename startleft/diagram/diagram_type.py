from startleft import paths
from startleft.provider import Provider


class DiagramType(str, Provider):
    VISIO = ("VISIO", "Visio", "diagram")
