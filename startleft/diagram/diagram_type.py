from startleft import paths
from startleft.provider import Provider


class DiagramType(str, Provider):
    VISIO = ("VISIO", "Visio", paths.default_visio_mapping_file, "diagram")
