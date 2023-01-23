import abc

from otm.otm.entity.representation import RepresentationElement
from slp_mtmt.slp_mtmt.entity.mtmt_entity import MTMEntity


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
