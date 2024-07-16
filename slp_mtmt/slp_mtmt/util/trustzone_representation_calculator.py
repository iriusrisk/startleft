from slp_mtmt.slp_mtmt.entity.mtmt_entity_border import MTMBorder
from slp_mtmt.slp_mtmt.util.representation_calculator import RepresentationCalculator


class TrustzoneRepresentationCalculator(RepresentationCalculator):

    def get_position(self) -> (int, int):
        if not isinstance(self.element, MTMBorder):
            return None, None

        return self.__get_relative_position() if isinstance(self.parent, MTMBorder) else self.__get_absolute_position()

    def get_size(self) -> (int, int):
        if isinstance(self.element, MTMBorder):
            return self.element.width, self.element.height
        return None, None

    def __get_absolute_position(self):
        return self.element.left, self.element.top

    def __get_relative_position(self):
        return self.element.left - self.parent.left, self.element.top - self.parent.top
