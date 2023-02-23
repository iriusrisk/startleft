from networkx import DiGraph

from otm.otm.entity.otm import OTM
from slp_tf.slp_tf.tfplan.transformers.tfplan_transformer import TfplanTransformer


class TfplanDataflowCreator(TfplanTransformer):

    def __init__(self, otm: OTM, graph: DiGraph):
        super().__init__(otm, graph)

    def transform(self):
        pass
