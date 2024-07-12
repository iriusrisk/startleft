from slp_mtmt.slp_mtmt.entity.mtmt_entity_border import MTMBorder
from slp_mtmt.slp_mtmt.util.representation_calculator import RepresentationCalculator


class ComponentRepresentationCalculator(RepresentationCalculator):

    def get_position(self) -> (int, int):
        return self.__get_border_position()

    def get_size(self) -> (int, int):
        return self.element.width, self.element.height

    def __get_border_position(self):
        if isinstance(self.parent, MTMBorder):
            x = self.element.left - self.parent.left
            y = self.element.top - self.parent.top
        else:
            x, y = self.element.left, self.element.top
        return x, y
