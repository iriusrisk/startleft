import abc

from networkx import DiGraph

from otm.otm.entity.otm import OTM
from slp_tf.slp_tf.tfplan.tfplan_objects import TfplanOTM


class TfplanTransformer(metaclass=abc.ABCMeta):
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
