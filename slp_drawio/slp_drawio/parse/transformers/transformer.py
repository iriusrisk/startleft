import abc

from slp_drawio.slp_drawio.objects.diagram_objects import Diagram


class Transformer(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'transform') and callable(subclass.transform)) or NotImplemented

    def __init__(self, diagram: Diagram):
        self.diagram: Diagram = diagram

    @abc.abstractmethod
    def transform(self):
        """ perform the necessary operations to transform and enrich the OTM """
        raise NotImplementedError
