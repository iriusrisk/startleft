from typing import List

from slp_drawio.slp_drawio.load.drawio_dict_utils import get_mx_cell_dataflows, get_dataflow_tags
from slp_drawio.slp_drawio.objects.diagram_objects import DiagramDataflow


class DiagramDataflowLoader:

    def __init__(self, source: dict):
        self._source: dict = source

    def load(self) -> [DiagramDataflow]:

        result: List[DiagramDataflow] = []

        mx_cell_dataflows = get_mx_cell_dataflows(self._source)
        for mx_cell in mx_cell_dataflows:
            if all(key in mx_cell for key in ['source', 'target']):
                result.append(DiagramDataflow(
                    dataflow_id=mx_cell.get('id'),
                    name=f'{mx_cell.get("id")}-dataflow',
                    source_node=mx_cell.get('source'),
                    destination_node=mx_cell.get('target'),
                    tags=get_dataflow_tags(mx_cell.get('id'), self._source)
                ))

        return result
