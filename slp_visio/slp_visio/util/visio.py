import re
from math import pi

from vsdx import Shape


def get_shape_text(shape: Shape) -> str:
    result = shape.text.replace('\n', '')
    if not result:
        result = get_child_shapes_text(shape.child_shapes)

    if not result:
        result = get_master_shape_text(shape)

    return (result or "").strip()


def get_master_shape_text(shape: Shape) -> str:
    if not shape.master_shape:
        return ""

    result = shape.master_shape.text.replace('\n', '')
    if not result:
        result = get_child_shapes_text(shape.master_shape.child_shapes)

    return (result or "").strip()


def get_child_shapes_text(shapes: [Shape]) -> str:
    if not shapes:
        return ""
    return "".join(shape.text.replace('\n', '') for shape in shapes)


def get_x_center(shape: Shape) -> float:
    return float(shape.center_x_y[0])


def get_y_center(shape: Shape) -> float:
    return float(shape.center_x_y[1])


def get_width(shape: Shape) -> float:
    if 'Width' in shape.cells:
        return float(shape.cells['Width'].value)

    if 'Width' in shape.master_shape.cells:
        return float(shape.master_shape.cells['Width'].value)


def get_height(shape: Shape) -> float:
    if 'Height' in shape.cells:
        return float(shape.cells['Height'].value)

    if 'Height' in shape.master_shape.cells:
        return float(shape.master_shape.cells['Height'].value)


def get_normalized_angle(shape: Shape) -> float:
    return normalize_angle(get_angle(shape))


def get_angle(shape: Shape) -> float:
    return float(shape.cells['Angle'].value)


def normalize_angle(angle: float) -> float:
    return angle + 2 * pi if angle < 0 else angle


def get_limits(shape: Shape) -> tuple:
    center_x = get_x_center(shape)
    center_y = get_y_center(shape)
    width = get_width(shape)
    height = get_height(shape)

    return (center_x - (width / 2), center_y - (height / 2)), \
           (center_x + (width / 2), center_y + (height / 2)) 


def normalize_label(label):
    if not label:
        return label

    # strip any leading or trailing \n or ' '
    label_normalized = label.strip(' \n')
    # replace by - any single middle '\n' or ' '
    label_normalized = label_normalized.replace('\n', '-')
    label_normalized = label_normalized.replace(' ', '-')
    # replace multiple in a row hyphens (2 or more) by a single one -
    label_normalized = re.sub('-{2,}', '-', label_normalized)

    return label_normalized
