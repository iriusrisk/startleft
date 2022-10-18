import abc

from slp_mtmt.slp_mtmt.entity.mtmt_entity_border import MTMBorder


class BorderTypeResolver(metaclass=abc.ABCMeta):
    """
    Formal Interface to resolve otm type for a mtmt element
    If a mtmt component can be two or more OTM component we should implement this class
    for the MTMT component and find the type
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
                hasattr(subclass, 'resolve') and callable(subclass.process)
                or NotImplemented)

    @abc.abstractmethod
    def resolve(self, map_: dict, border: MTMBorder) -> str:
        """Finds the otm type"""
        raise NotImplementedError
