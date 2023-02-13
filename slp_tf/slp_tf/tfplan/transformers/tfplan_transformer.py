import abc

from networkx import DiGraph

from otm.otm.entity.otm import Otm


class TfplanTransformer(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'transform') and callable(subclass.transform)) or NotImplemented

    def __init__(self, otm: Otm, graph: DiGraph):
        self.otm: Otm = otm
        self.graph: DiGraph = graph

    @abc.abstractmethod
    def transform(self):
        """ perform the necessary operations to transform and enrich the OTM """
        raise NotImplementedError
