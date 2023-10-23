from typing import Dict, List, Any


def __get_as_mx_point_in_mx_geometry(attr: str, mx_geometry: Dict):
    if 'mxPoint' not in mx_geometry:
        return
    mx_points = [mx_geometry['mxPoint']] if isinstance(mx_geometry['mxPoint'], dict) else mx_geometry['mxPoint']

    for mx_point in mx_points:
        if mx_point.get('as') == attr:
            return mx_point


def __is_mx_cell_dataflow(mx_cell):
    if 'mxGeometry' not in mx_cell:
        return False

    source = mx_cell.get('source') or __get_as_mx_point_in_mx_geometry('sourcePoint', mx_cell['mxGeometry'])
    target = mx_cell.get('target') or __get_as_mx_point_in_mx_geometry('targetPoint', mx_cell['mxGeometry'])

    return source and target


def __is_mx_cell_component(mx_cell: Dict):
    if 'mxGeometry' not in mx_cell:
        return False
    return not __is_mx_cell_dataflow(mx_cell)


def __get_mx_cell_from_source(source):
    return source.get("mxfile", {}).get("diagram", {}).get("mxGraphModel", {}).get("root", {}).get("mxCell", [])


def get_components_from_source(source) -> List[Dict]:
    return list(filter(lambda c: __is_mx_cell_component(c), __get_mx_cell_from_source(source)))


def get_dataflows_from_source(source) -> List[Dict]:
    return list(filter(lambda c: __is_mx_cell_dataflow(c), __get_mx_cell_from_source(source)))


def is_multiple_pages(source):
    diagram_pages = source.get("mxfile", {}).get("diagram", None)
    return len(diagram_pages) > 1 if isinstance(diagram_pages, list) else False


def get_attributes(mx_cell: Dict) -> Dict[str, Any]:
    attributes: Dict[str, Any] = {}
    styles = mx_cell.get('style', '').split(';')
    for style in styles:
        if not style:
            continue
        key, value = style, None
        if '=' in style:
            key, value = style.split('=')
        attributes[key] = value

    return attributes
