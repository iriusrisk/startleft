from typing import List, Optional

from otm.otm.entity.component import Component
from otm.otm.entity.otm import OTM
from otm.otm.entity.representation import RepresentationElement
from otm.otm.entity.trustzone import Trustzone

TZ_PADDING = 30


def __get_component_representation(component: Component):
    return component.representations[0] if component.representations and len(component.representations) > 0 else None


def __calculate_tz_representation_by_components(
        representation_id, tz: Trustzone, components: List[Component]) -> Optional[RepresentationElement]:
    """
    Calculate the trustzone representation:
    The coordinates x, y starts as 0,0 in the top left corner of the diagram
    :param representation_id:
    :param tz:
    :param components:
    :return:
    """
    left_x, right_x, top_y, bottom_y = (None,)*4
    for component in components:
        representation = __get_component_representation(component)
        if not representation:
            continue

        x, y = representation.position['x'], representation.position['y']
        width, height = representation.size['width'], representation.size['height']

        if not left_x or x < left_x:
            left_x = x
        if not right_x or right_x < (x + width):
            right_x = (x + width)

        if not top_y or y < top_y:
            top_y = y
        if not bottom_y or bottom_y < (y + height):
            bottom_y = (y + height)

    if not left_x and not right_x and not top_y and not bottom_y:
        return

    return RepresentationElement(
        id_=f'{tz.id}-representation',
        name=f'{tz.name} Representation',
        representation=representation_id,
        position={'x': left_x - TZ_PADDING, 'y': top_y - TZ_PADDING},
        size={'width': (right_x - left_x) + (TZ_PADDING*2), 'height': (bottom_y - top_y) + (TZ_PADDING*2)}
    )


def __calculate_relative_representation_by_tz(tz: Trustzone, tz_components: List[Component]):
    """
    Calculates the relative component coordinates by the given trustzone
    :param tz:
    :param tz_components:
    :return:
    """
    tz_position_x, tz_position_y = tz.representations[0].position['x'], tz.representations[0].position['y']

    for component in tz_components:
        c_representation = __get_component_representation(component)
        if not c_representation:
            continue
        c_representation.position['x'] -= tz_position_x
        c_representation.position['y'] -= tz_position_y


def calculate_tz_representation(otm: OTM, representation_id):
    for tz in otm.trustzones:
        if tz.representations and len(tz.representations) > 0:
            continue
        tz_components = list(filter(lambda component: component.parent == tz.id, otm.components))
        representation = __calculate_tz_representation_by_components(representation_id, tz, tz_components)
        if representation:
            tz.representations = [representation]
            __calculate_relative_representation_by_tz(tz, tz_components)
