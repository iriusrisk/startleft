from networkx import DiGraph

from slp_tf.slp_tf.tfplan.transformers.tfplan_transformer import TfplanTransformer
from slp_tf.slp_tf.tfplan.tfplan_objects import TfplanOTM


class TfplanSingletonTransformer(TfplanTransformer):

    def __init__(self, otm: TfplanOTM, graph: DiGraph):
        super().__init__(otm, graph)

    def transform(self):
        pass
