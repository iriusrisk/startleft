import abc

from networkx import DiGraph

from slp_tfplan.slp_tfplan.objects.tfplan_objects import TfplanOTM


class Transformer(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'transform') and callable(subclass.transform)) or NotImplemented

    def __init__(self, otm: TfplanOTM, graph: DiGraph = None):
        self.otm: TfplanOTM = otm
        self.graph: DiGraph = graph

    @abc.abstractmethod
    def transform(self):
        """ perform the necessary operations to transform and enrich the OTM """
        raise NotImplementedError
