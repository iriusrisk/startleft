import re
from typing import Optional

from slp_drawio.slp_drawio.load.stencil_extractors import MxCell, register_extractor

_AWS_EQUIVALENCES = {
    'aws.group': 'grIcon',
    'aws.groupCenter': 'grIcon',
    'aws.resourceIcon': 'resIcon',
    'aws.productIcon': 'prIcon',
}


def _remove_mxgraph(text: str) -> str:
    return re.sub(r"mxgraph\.", "", text)


def _remove_mxgraph_aws(text: str) -> str:
    return re.sub(r"aws\d\.", "aws.", text)


def _normalize_shape_type(text: str) -> str:
    text = _remove_mxgraph(text)
    text = _remove_mxgraph_aws(text)
    return text


def _get_shape_attribute(mx_cell: MxCell, attr) -> Optional[str]:
    style = mx_cell.get("style", "")
    for part in style.split(";"):
        if part.startswith(attr + "="):
            return part.split("=")[1]
    return None


@register_extractor
def extract_aws_type(mx_cell: MxCell, attr: str = 'shape') -> Optional[str]:
    shape_type = _get_shape_attribute(mx_cell, attr)
    if not shape_type:
        return None
    shape_type = _normalize_shape_type(shape_type)
    if shape_type in _AWS_EQUIVALENCES:
        shape_type = extract_aws_type(mx_cell, _AWS_EQUIVALENCES[shape_type])
    return shape_type
