import abc

from otm.otm.entity.representation import RepresentationElement
from slp_mtmt.slp_mtmt.entity.mtmt_entity import MTMEntity

# TODO: Make the scale of the output representations parametrizable
IRIUSRISK_SMALLEST_COMPONENT_SIZE = 82
MTMT_DEFAULT_SIZE = 100
SCALE_FACTOR: float = (IRIUSRISK_SMALLEST_COMPONENT_SIZE / MTMT_DEFAULT_SIZE)


def scale_to_int(value: float) -> int:
    return round(value * SCALE_FACTOR)


class RepresentationCalculator(metaclass=abc.ABCMeta):
    """
    Formal Interface to calculate an OTM RepresentationElement from a MTMEntity
    """

    def __init__(self, representation: str, element: MTMEntity, parent=None):
        self.element: MTMEntity = element
        self.parent = parent
        self.representation = representation

    @classmethod
    def __subclasshook__(cls, subclass):
        return hasattr(subclass, 'get_position') and callable(subclass.build_otm) or NotImplemented

    @abc.abstractmethod
    def get_position(self) -> (int, int):
        raise NotImplementedError

    @abc.abstractmethod
    def get_size(self) -> (int, int):
        raise NotImplementedError

    def scale_representation(self, representation: RepresentationElement) -> int:
        original_width = representation.size['width']
        original_height = representation.size['height']
        scaled_width = scale_to_int(original_width)
        scaled_height = scale_to_int(original_height)
        representation.size['width'] = scaled_width
        representation.size['height'] = scaled_height

    def calculate_representation(self):
        x, y = self.get_position()
        width, height = self.get_size()
        if not x or not y or not width or not height:
            return
        representation_id = self.element.id + '-representation'
        representation_name = self.element.name + ' Representation'
        position = {"x": x, "y": y}
        size = {"width": width, "height": height}
        return RepresentationElement(id_=representation_id, name=representation_name,
                                     representation=self.representation, position=position, size=size)
