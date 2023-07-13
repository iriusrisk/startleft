import string
from math import pi

from vsdx import Shape

import re


def get_shape_text(shape: Shape) -> str:
    result = shape.text
    if not result:
        result = get_child_shapes_text(shape.child_shapes)

    if not result:
        result = get_master_shape_text(shape)

    return (result or "").strip()


def get_master_shape_text(shape: Shape) -> str:
    if not shape.master_shape:
        return ""

    result = shape.master_shape.text
    if not result:
        result = get_child_shapes_text(shape.master_shape.child_shapes)

    return (result or "").strip()


def get_unique_id_text(shape: Shape) -> str:
    if not shape.master_page or not shape.master_page.master_unique_id:
        return ""

    unique_id = shape.master_page.master_unique_id.strip()
    return normalize_unique_id(unique_id)


def get_child_shapes_text(shapes: [Shape]) -> str:
    if not shapes:
        return ""
    return "".join(shape.text for shape in shapes)


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

# These expressions are secure, so we can use the standard re lib by performance reason
LUCID_AWS_YEARS_PATTERN = re.compile(r'_?(?:2017|AWS19|AWS19_v2|AWS2021)$')
NON_PRINTABLE_CHARS_PATTERN = re.compile(f'[^{re.escape(string.printable)}]')
ANY_SPACE_PATTERN = re.compile(r'\s+')

# Notice that the order of the functions is relevant
normalize_functions = [
    # remove year from Lucidchart AWS stencils
    lambda label: LUCID_AWS_YEARS_PATTERN.sub('', label),
    # replace by a space any non-printable character
    lambda label: NON_PRINTABLE_CHARS_PATTERN.sub(' ', label),
    # replace multiple spaces in a row (2 or more) by a single one
    lambda label: ANY_SPACE_PATTERN.sub(' ', label),
    # strip any leading or trailing space
    lambda label: label.strip()
]


def normalize_label(label: str) -> str:
    if not label:
        return label

    for normalize_function in normalize_functions:
        label = normalize_function(label)

    return label


def normalize_unique_id(unique_id):
    return re.sub("[{}]", "", unique_id) if unique_id else ""
