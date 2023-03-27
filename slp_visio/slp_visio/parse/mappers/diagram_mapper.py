import abc

from otm.otm.entity.parent_type import ParentType
from slp_visio.slp_visio.load.objects.diagram_objects import DiagramComponent


class DiagramMapper(metaclass=abc.ABCMeta):

    def _calculate_parent_type(self, component: DiagramComponent) -> ParentType:
        if not component.parent or component.parent.name in self._get_trustzone_mappings().keys():
            return ParentType.TRUST_ZONE
        else:
            return ParentType.COMPONENT

    @abc.abstractmethod
    def _get_trustzone_mappings(self):
        """get the trustzone_mappings implementation"""
        raise NotImplementedError
