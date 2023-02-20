import logging

from otm.otm.entity.otm import OTM

logger = logging.getLogger(__name__)


class OTMPruner:

    def __init__(self, otm: OTM):
        self.otm = otm
        self.otm_component_ids = [c.id for c in self.otm.components]

    def prune_orphan_dataflows(self):
        dataflows = []
        for df in self.otm.dataflows:
            if df.source_node in self.otm_component_ids and df.destination_node in self.otm_component_ids:
                dataflows.append(df)
            else:
                logger.warning(f'The dataflow {df} has been removed because connects an element that is not a '
                               f'component')
        self.otm.dataflows = dataflows
