import re
from typing import List, Dict

from otm.otm.entity.representation import RepresentationElement
from slp_base import LoadingDiagramFileError
from slp_drawio.slp_drawio.load.drawio_dict_utils import is_multiple_pages, \
    get_attributes, get_position, get_size, get_mx_cell_components
from slp_drawio.slp_drawio.objects.diagram_objects import DiagramComponent

__CALCULATE_SHAPE_TYPE_EQUIVALENCES = resource_types_equivalences = {
    'aws.group': 'grIcon',
    'aws.groupCenter': 'grIcon',
    'aws.resourceIcon': 'resIcon',
    'aws.productIcon': 'prIcon'
}


def __remove_mxgraph_aws(text):
    return re.sub(r"aws\d.", "aws.", text)


def __remove_mxgraph(text):
    return re.sub(r"mxgraph.", "", text)


def __normalize_shape_type(text):
    for normalize_function in [__remove_mxgraph, __remove_mxgraph_aws]:
        text = normalize_function(text)

    return text


def _calculate_shape_type(mx_cell: Dict, attr: str = 'shape'):
    shape = get_attributes(mx_cell).get(attr)
    if not shape:
        return
    shape_type = __normalize_shape_type(shape)
    if shape_type in __CALCULATE_SHAPE_TYPE_EQUIVALENCES:
        shape_type = _calculate_shape_type(mx_cell, __CALCULATE_SHAPE_TYPE_EQUIVALENCES.get(shape_type))

    return shape_type


def _get_shape_parent_id(mx_cell: Dict, mx_cell_components: List[Dict]):
    return mx_cell.get('parent') \
        if any(item.get('id') == mx_cell.get('parent') for item in mx_cell_components) else None


def _get_shape_name(mx_cell: Dict):
    name = mx_cell.get('value')
    if not name:
        name = _calculate_shape_type(mx_cell) or ''
        if '.' in name:
            name = name.split('.')[-1]
        name = name.replace('_', ' ')
    if not name:
        name = 'N/A'
    if len(name) == 1:
        name = f'_{name}'
    return name


class DiagramComponentLoader:

    def __init__(self, project_id: str, source: dict):
        self._project_id = project_id
        self._source: dict = source

    def load(self) -> [DiagramComponent]:
        if is_multiple_pages(self._source):
            raise LoadingDiagramFileError(
                'Diagram file is not valid', 'Diagram File is not compatible',
                'DrawIO processor does not accept diagrams with multiple pages')

        result: List[DiagramComponent] = []

        mx_cell_components = get_mx_cell_components(self._source)
        for mx_cell in mx_cell_components:
            result.append(DiagramComponent(
                id=mx_cell.get('id'),
                name=_get_shape_name(mx_cell),
                shape_type=_calculate_shape_type(mx_cell),
                shape_parent_id=_get_shape_parent_id(mx_cell, mx_cell_components),
                representations=[self._get_representation_element(mx_cell)]
            ))

        return result

    def _get_representation_element(self, mx_cell: Dict) -> RepresentationElement:
        return RepresentationElement(
            id_=f"{mx_cell.get('id')}-diagram",
            name=f"{mx_cell.get('id')} Representation",
            representation=f"{self._project_id}-diagram",
            position=get_position(mx_cell),
            size=get_size(mx_cell),
            attributes={'style': mx_cell.get('style')}
        )
