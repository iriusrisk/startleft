import abc
from typing import Optional

from vsdx import Shape

from slp_visio.slp_visio.load.objects.diagram_objects import DiagramComponent
from slp_visio.slp_visio.load.representation.visio_shape_representer import VisioShapeRepresenter
from slp_visio.slp_visio.load.strategies.strategy import Strategy


class CreateComponentStrategy(Strategy):
    """
    Formal Interface to create an OTM Component from a vsdx shape
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
                hasattr(subclass, 'create_component') and callable(subclass.process)
                or NotImplemented)

    @abc.abstractmethod
    def create_component(self, shape: Shape, origin=None, representer: VisioShapeRepresenter = None) \
            -> Optional[DiagramComponent]:
        """creates the OTM Component from the vsdx shape"""
        raise NotImplementedError
