from typing import List, Tuple, Union

from otm.otm.entity.component import Component
from otm.otm.entity.otm import OTM
from otm.otm.entity.representation import RepresentationElement
from otm.otm.entity.trustzone import Trustzone
from otm.otm.util.representation import build_size, build_position, make_relative

TZ_PADDING = 30


def _get_trustzone_components(trustzone_id: str, components: List[Component]):
    return list(filter(lambda component: component.parent == trustzone_id, components))


def _get_first_representation(component: Component):
    return component.representations[0] if component.representations and len(component.representations) > 0 else None


def calculate_missing_trustzones_representations(otm: OTM, representation_id):
    for trustzone in otm.trustzones:
        if not trustzone.representations:
            tz_components = _get_trustzone_components(trustzone.id, otm.components)
            TrustZoneRepresentationCalculator(representation_id, trustzone, tz_components).calculate()


class TrustZoneRepresentationCalculator:
    def __init__(self, representation_id: str, trustzone: Trustzone, children: List[Union[Component, Trustzone]]):
        self.representation_id = representation_id
        self.trustzone = trustzone
        self.children = children

        self.child_representation = list(filter(lambda r: r, map(_get_first_representation, children)))

    def calculate(self):
        if self.child_representation:
            self.trustzone.representations = [self.__calculate_trustzone_representation_by_children()]
            self.__make_components_representations_relative()

    def __calculate_trustzone_representation_by_children(self):
        left_x, right_x, top_y, bottom_y = self.__calculate_trustzone_limits_by_children()

        return RepresentationElement(
            id_=f'{self.trustzone.id}-representation',
            name=f'{self.trustzone.name} Representation',
            representation=self.representation_id,
            position=build_position(left_x, top_y, TZ_PADDING),
            size=build_size(left_x, right_x, top_y, bottom_y, TZ_PADDING)
        )

    def __calculate_trustzone_limits_by_children(self) -> Tuple:
        """
        Calculate the trustzone representation by the position of its children components.
        The coordinates x, y starts as 0,0 in the top left corner of the diagram
        """
        left_x, right_x, top_y, bottom_y = (None,) * 4

        for representation in self.child_representation:
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

        return left_x, right_x, top_y, bottom_y

    def __make_components_representations_relative(self):
        tz_position = self.trustzone.representations[0].position
        for child in self.children:
            make_relative(_get_first_representation(child), tz_position)
