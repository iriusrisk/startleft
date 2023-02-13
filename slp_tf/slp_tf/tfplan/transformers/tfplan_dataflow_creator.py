from networkx import DiGraph

from otm.otm.entity.otm import Otm
from slp_tf.slp_tf.tfplan.transformers.tfplan_transformer import TfplanTransformer


class TfplanDataflowCreator(TfplanTransformer):

    def __init__(self, otm: Otm, graph: DiGraph):
        super().__init__(otm, graph)

    def transform(self):
        pass
