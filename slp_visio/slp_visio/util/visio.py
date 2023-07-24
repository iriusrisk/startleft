import re
from functools import singledispatch
from math import pi

from vsdx import Shape

from slp_visio.slp_visio.parse.shape_position_calculator import ShapePositionCalculator

@singledispatch
def get_shape_text(shape):
    if not shape:
        return ""
    result = shape.text

    if not result:
        result = get_master_shape_text(shape)

    return (result or "").strip()

@get_shape_text.register(list)
def get_shape_text_from_list(shapes: [Shape]) -> str:
    if not shapes:
        return ""
    return "".join(shape.text or "" for shape in shapes)



def get_master_shape_text(shape: Shape) -> str:
    if not shape.master_shape:
        return ""

    result = shape.master_shape.text

    return (result or "").strip()


def get_unique_id_text(shape: Shape) -> str:
    if not shape.master_page or not shape.master_page.master_unique_id:
        return ""

    unique_id = shape.master_page.master_unique_id.strip()
    return normalize_unique_id(unique_id)

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
    calculator = ShapePositionCalculator(shape)
    center_x, center_y = calculator.get_absolute_center()
    width = get_width(shape)
    height = get_height(shape)

    return (center_x - (width / 2), center_y - (height / 2)), \
        (center_x + (width / 2), center_y + (height / 2))


# Notice that the order of the functions is relevant
normalize_functions = [
    # remove year from Lucidchart AWS stencils
    lambda label: re.sub(r'_?(2017|AWS19|AWS19_v2|AWS2021)$', '', label),
    # replace by ' ' any '\n'
    lambda label: label.replace('\n', ' '),
    # replace multiple spaces in a row (2 or more) by a single one
    lambda label: re.sub(r'\s+', ' ', label),
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
