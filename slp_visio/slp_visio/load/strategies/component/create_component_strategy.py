import abc
from typing import Optional

from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer
from vsdx import Shape

from slp_visio.slp_visio.load.objects.diagram_objects import DiagramComponent
from slp_visio.slp_visio.load.representation.visio_shape_representer import VisioShapeRepresenter


class CreateComponentStrategy:
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


class CreateComponentStrategyContainer(DeclarativeContainer):
    """
    CreateComponentStrategy implementations is grouped depending on the source tool:
    Lucid or Visio
    """
    visio_strategies = providers.List()
