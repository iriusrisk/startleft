from slp_mtmt.slp_mtmt.entity.mtmt_entity_border import MTMBorder
from slp_mtmt.slp_mtmt.util.representation_calculator import RepresentationCalculator


class TrustzoneRepresentationCalculator(RepresentationCalculator):

    def get_position(self) -> (int, int):
        if isinstance(self.element, MTMBorder):
            return self.__get_border_position()
        return None, None

    def get_size(self) -> (int, int):
        if isinstance(self.element, MTMBorder):
            return self.element.width, self.element.height
        return None, None

    def __get_border_position(self):
        return self.element.left, self.element.top
