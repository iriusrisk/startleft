from slp_mtmt.slp_mtmt.util.representation_calculator import RepresentationCalculator


class ComponentRepresentationCalculator(RepresentationCalculator):

    def get_position(self) -> (int, int):
        if self.parent:
            x = self.element.left - self.parent.left
            y = self.element.top - self.parent.top
        else:
            x, y = self.element.left, self.element.top
        return x, y

    def get_size(self) -> (int, int):
        return self.element.width, self.element.height
