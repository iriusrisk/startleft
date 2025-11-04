from otm.otm.entity.representation import RepresentationElement

from slp_drawio.slp_drawio.load.drawio_dict_utils import get_position, get_size, get_mx_cell_components
from slp_drawio.slp_drawio.load.drawio_mxcell_utils import get_cell_name, get_cell_parent_id, get_cell_style
from slp_drawio.slp_drawio.load.stencil_extractors import extract_stencil_type
from slp_drawio.slp_drawio.objects.diagram_objects import DiagramComponent


class DiagramComponentLoader:

    def __init__(self, project_id: str, source: dict):
        self._project_id = project_id
        self._source: dict = source

    def load(self) -> list[DiagramComponent]:
        result: list[DiagramComponent] = []

        mx_cell_components = get_mx_cell_components(self._source)
        for mx_cell in mx_cell_components:
            result.append(DiagramComponent(
                id=mx_cell.get('id'),
                name=get_cell_name(mx_cell),
                shape_type=extract_stencil_type(mx_cell),
                shape_parent_id=get_cell_parent_id(mx_cell, mx_cell_components),
                representations=[self._get_representation_element(mx_cell)]
            ))

        return result

    def _get_representation_element(self, mx_cell: dict) -> RepresentationElement:
        return RepresentationElement(
            id_=f"{mx_cell.get('id')}-diagram",
            name=f"{mx_cell.get('id')} Representation",
            representation=f"{self._project_id}-diagram",
            position=get_position(mx_cell),
            size=get_size(mx_cell),
            attributes={'style': get_cell_style(mx_cell)}
        )
