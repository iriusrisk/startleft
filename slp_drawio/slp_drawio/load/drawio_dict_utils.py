from typing import Any, Optional


def __get_as_mx_point_in_mx_geometry(attr: str, mx_geometry: dict):
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


def __is_mx_cell_component(mx_cell: dict):
    mx_geometry = mx_cell.get('mxGeometry', {})
    if not all(key in mx_geometry for key in ['height', 'width']):
        return False
    return not __is_mx_cell_dataflow(mx_cell)


def __get_root_element(source) -> dict:
    return source.get("mxfile", {}).get("diagram", {}).get("mxGraphModel",
                                                           source.get("mxGraphModel", {})).get("root", {})


def __process_object_elements(root: dict, element_keys: list[str]) -> list[dict]:
    mx_cells = []
    for key in element_keys:
        elements = root.get(key, [])
        if not isinstance(elements, list):
            elements = [elements]

        for element in elements:
            mx_cell = element.get("mxCell", {})
            if mx_cell:
                mx_cell["id"] = element.get("id")
                mx_cell["value"] = mx_cell.get("value") or element.get("value")
                mx_cell["label"] = mx_cell.get("label") or element.get("label")
                mx_cells.append(mx_cell)
    return mx_cells


def __process_standalone_cells(root: dict) -> list[dict]:
    standalone_cells = root.get("mxCell", [])
    if isinstance(standalone_cells, dict):
        standalone_cells = [standalone_cells]
    return standalone_cells


def __get_mx_cells(source) -> list[dict]:
    root = __get_root_element(source)
    mx_cells = __process_object_elements(root, ['object', 'UserObject'])
    mx_cells.extend(__process_standalone_cells(root))
    return mx_cells


def get_mx_cell_components(source) -> list[dict]:
    return list(filter(lambda c: __is_mx_cell_component(c), __get_mx_cells(source)))


def get_mx_cell_dataflows(source) -> list[dict]:
    return list(filter(lambda c: __is_mx_cell_dataflow(c), __get_mx_cells(source)))


def get_dataflow_tags(dataflow_id: str, source) -> list[str]:
    tags: list[str] = []

    for mx_cell in __get_mx_cells(source):
        if dataflow_id == mx_cell.get('parent') and 'value' in mx_cell:
            tags.append(mx_cell['value'])

    return tags


def get_diagram_size(source) -> Optional[dict]:
    model = source.get("mxfile", {}).get("diagram", {}).get("mxGraphModel", source.get("mxGraphModel", {}))
    if model:
        height = model.get('pageHeight', None)
        width = model.get('pageWidth', None)

        try:
            return {'width': int(width), 'height': int(height)} if height and width else None
        except ValueError:
            return None


def is_multiple_pages(source):
    diagram_pages = source.get("mxfile", {}).get("diagram", None)
    return len(diagram_pages) > 1 if isinstance(diagram_pages, list) else False


def get_attributes(mx_cell: dict) -> dict[str, Any]:
    attributes: dict[str, Any] = {}
    styles = mx_cell.get('style', '').split(';')
    for style in styles:
        if not style:
            continue
        key, value = style, None
        if '=' in style:
            key, value = style.split('=', 1)
        attributes[key] = value

    return attributes


def __str_to_int(value: str):
    return int(round(float(value), 0))


def get_position(mx_cell: dict) -> dict[str, float]:
    mx_geometry = mx_cell.get('mxGeometry', {})
    return {
        'x': __str_to_int(mx_geometry.get('x', '0')),
        'y': __str_to_int(mx_geometry.get('y', '0')),
    }


def get_size(mx_cell: dict) -> dict[str, float]:
    mx_geometry = mx_cell.get('mxGeometry', {})
    return {
        'height': __str_to_int(mx_geometry.get('height')),
        'width': __str_to_int(mx_geometry.get('width')),
    }